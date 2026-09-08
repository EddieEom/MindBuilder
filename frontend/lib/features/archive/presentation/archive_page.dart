import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../core/widgets/feature_widgets.dart';
import '../data/archive_repository.dart';

const archiveTypes = {
  'SCAN_COMPLETED': 'Mind Scan',
  'PATTERN_ANALYZED': 'Pattern',
  'GROWTH_ANALYZED': 'Growth',
  'LIFEMAP_CREATED': 'Life Map',
  'IDENTITY_CREATED': 'Identity',
  'OS_UPDATED': 'Human OS',
  'SEED_CREATED': 'Seed',
};

class ArchivePage extends ConsumerStatefulWidget {
  const ArchivePage({super.key});
  @override
  ConsumerState<ArchivePage> createState() => _ArchivePageState();
}

class _ArchivePageState extends ConsumerState<ArchivePage> {
  int _tab = 0, _generation = 0, _offset = 0;
  DateTime _date = DateTime.now();
  String? _type;
  String _search = '';
  bool _searchOpen = false, _loading = true, _hasMore = false;
  Object? _error;
  List<ArchiveEvent> _events = [];
  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load({bool more = false}) async {
    final generation = ++_generation;
    final offset = more ? _offset : 0;
    setState(() {
      _loading = true;
      _error = null;
      if (!more) {
        _events = [];
        _offset = 0;
      }
    });
    try {
      final events = await ref
          .read(archiveRepositoryProvider)
          .events(tab: _tab, date: _date, type: _type, offset: offset);
      if (!mounted || generation != _generation) return;
      setState(() {
        _events = more
            ? [
                ..._events,
                ...events.where((e) => !_events.any((old) => old.id == e.id)),
              ]
            : events;
        _offset = offset + events.length;
        _hasMore = _tab != 1 && events.length == 30;
        _loading = false;
      });
    } catch (error) {
      if (mounted && generation == _generation) {
        setState(() {
          _error = error;
          _loading = false;
        });
      }
    }
  }

  Future<void> _pickDate() async {
    final date = await showDatePicker(
      context: context,
      initialDate: _date,
      firstDate: DateTime(2000),
      lastDate: DateTime.now(),
    );
    if (date != null && mounted) {
      setState(() {
        _date = date;
        _tab = 1;
      });
      await _load();
    }
  }

  @override
  Widget build(BuildContext context) {
    final visible = _events
        .where(
          (e) => '${e.title} ${e.summary ?? ''}'.toLowerCase().contains(
            _search.toLowerCase(),
          ),
        )
        .toList();
    return FeaturePage(
      title: 'Archive',
      icon: Icons.inventory_2_outlined,
      subtitle: '당신의 모든 기록과 성장의 흔적을 모아보세요.',
      actions: [
        IconButton(
          tooltip: '기록 검색',
          onPressed: () => setState(() {
            _searchOpen = !_searchOpen;
            _search = '';
          }),
          icon: const Icon(Icons.search, size: 19),
        ),
        PopupMenuButton<String>(
          tooltip: '기록 유형 필터',
          icon: const Icon(Icons.filter_alt_outlined, size: 19),
          onSelected: (value) {
            setState(() {
              _tab = 0;
              _type = value.isEmpty ? null : value;
            });
            _load();
          },
          itemBuilder: (_) => [
            const PopupMenuItem(value: '', child: Text('모든 유형')),
            ...archiveTypes.entries.map(
              (e) => PopupMenuItem(value: e.key, child: Text(e.value)),
            ),
          ],
        ),
      ],
      bottom: SafeArea(
        top: false,
        child: Container(
          color: Theme.of(context).cardColor,
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: [
              _nav(context, Icons.home_outlined, '홈', '/dashboard'),
              _nav(context, Icons.spa_outlined, 'Growth', '/growth'),
              _nav(context, Icons.hub_outlined, 'Life Map', '/lifemap'),
              _nav(context, Icons.person_outline, 'Identity', '/identity'),
              _nav(context, Icons.psychology_outlined, 'HOS', '/hos'),
            ],
          ),
        ),
      ),
      child: Column(
        children: [
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 20),
            child: Row(
              children: List.generate(
                4,
                (i) => Expanded(
                  child: TextButton(
                    style: TextButton.styleFrom(
                      backgroundColor: _tab == i ? featurePurple : null,
                      foregroundColor: _tab == i ? Colors.white : featureMuted,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(7),
                      ),
                      padding: const EdgeInsets.symmetric(horizontal: 2),
                    ),
                    onPressed: () {
                      setState(() {
                        _tab = i;
                        _type = null;
                      });
                      _load();
                    },
                    child: Text(
                      ['전체 기록', '날짜별 조회', '성장 타임라인', '최근 HOS'][i],
                      style: const TextStyle(fontSize: 10),
                    ),
                  ),
                ),
              ),
            ),
          ),
          if (_searchOpen)
            Padding(
              padding: const EdgeInsets.fromLTRB(22, 10, 22, 0),
              child: TextField(
                autofocus: true,
                onChanged: (value) => setState(() => _search = value),
                decoration: const InputDecoration(
                  hintText: '불러온 기록에서 검색',
                  prefixIcon: Icon(Icons.search),
                ),
              ),
            ),
          if (_tab == 1)
            TextButton.icon(
              onPressed: _pickDate,
              icon: const Icon(Icons.calendar_month, size: 17),
              label: Text(displayDate(_date)),
            ),
          if (_type != null)
            Padding(
              padding: const EdgeInsets.only(top: 8),
              child: FeatureTags([archiveTypes[_type] ?? _type!]),
            ),
          Expanded(
            child: RefreshIndicator(
              onRefresh: () async {
                ref.invalidate(archiveSummaryProvider);
                await _load();
              },
              child: ListView(
                padding: const EdgeInsets.all(22),
                physics: const AlwaysScrollableScrollPhysics(),
                children: [
                  FeatureSection(
                    '전체 기록 요약',
                    child: ref
                        .watch(archiveSummaryProvider)
                        .when(
                          loading: () => const LinearProgressIndicator(),
                          error: (e, _) => TextButton(
                            onPressed: () =>
                                ref.invalidate(archiveSummaryProvider),
                            child: const Text('요약 다시 불러오기'),
                          ),
                          data: (counts) => Row(
                            children: [
                              _count(
                                'Scan 기록',
                                counts['SCAN_COMPLETED'] ?? 0,
                                const Color(0xFF8773EA),
                              ),
                              _count(
                                'Growth 분석',
                                counts['GROWTH_ANALYZED'] ?? 0,
                                const Color(0xFF76B68D),
                              ),
                              _count(
                                '전체 기록',
                                counts.values.fold(0, (a, b) => a + b),
                                const Color(0xFFECA664),
                              ),
                              _count(
                                'HOS 기록',
                                counts['OS_UPDATED'] ?? 0,
                                const Color(0xFF8C86DB),
                              ),
                            ],
                          ),
                        ),
                  ),
                  Padding(
                    padding: const EdgeInsets.symmetric(vertical: 10),
                    child: Row(
                      children: [
                        const Expanded(
                          child: Text(
                            '최근 기록',
                            style: TextStyle(
                              fontSize: 13,
                              fontWeight: FontWeight.w700,
                            ),
                          ),
                        ),
                        Text(
                          '${_events.length}개 불러옴',
                          style: const TextStyle(
                            fontSize: 10,
                            color: featureMuted,
                          ),
                        ),
                      ],
                    ),
                  ),
                  if (_loading && _events.isEmpty)
                    const Padding(
                      padding: EdgeInsets.all(35),
                      child: Center(child: CircularProgressIndicator()),
                    ),
                  if (_error != null)
                    FeatureCard(
                      child: Column(
                        children: [
                          Text(
                            requestMessage(_error!),
                            style: const TextStyle(fontSize: 12),
                          ),
                          TextButton(
                            onPressed: () => _load(more: _events.isNotEmpty),
                            child: const Text('다시 시도'),
                          ),
                        ],
                      ),
                    ),
                  if (!_loading && _error == null && visible.isEmpty)
                    const FeatureEmpty('조건에 맞는 기록이 없어요.'),
                  ...visible.map((event) => _eventCard(context, event)),
                  if (_hasMore)
                    TextButton(
                      onPressed: _loading ? null : () => _load(more: true),
                      child: Text(_loading ? '불러오는 중…' : '기록 더 보기'),
                    ),
                  FeatureCard(
                    color: const Color(0xFFF2EFFF),
                    child: ListTile(
                      contentPadding: EdgeInsets.zero,
                      leading: const Icon(
                        Icons.calendar_month,
                        color: featurePurple,
                      ),
                      title: const Text(
                        '날짜별로 기록 찾아보기',
                        style: TextStyle(
                          fontSize: 12,
                          color: featurePurple,
                          fontWeight: FontWeight.w600,
                        ),
                      ),
                      trailing: const Icon(
                        Icons.chevron_right,
                        color: featurePurple,
                      ),
                      onTap: _pickDate,
                    ),
                  ),
                  const FeatureCard(
                    color: Color(0xFFF8F6FF),
                    child: Row(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Icon(
                          Icons.auto_awesome,
                          color: featurePurple,
                          size: 21,
                        ),
                        SizedBox(width: 12),
                        Expanded(
                          child: Text(
                            '기록이 쌓일수록 패턴이 선명해져요\n\n지난 생각과 오늘의 변화를 함께 살펴보세요.',
                            style: TextStyle(fontSize: 12, height: 1.7),
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _count(String label, int value, Color color) => Expanded(
    child: Column(
      children: [
        Text(label, style: const TextStyle(fontSize: 8, color: featureMuted)),
        const SizedBox(height: 8),
        Text(
          '$value',
          style: TextStyle(
            fontSize: 18,
            fontWeight: FontWeight.w800,
            color: color,
          ),
        ),
      ],
    ),
  );
  Widget _nav(
    BuildContext context,
    IconData icon,
    String label,
    String route,
  ) => InkWell(
    onTap: () => context.go(route),
    child: Padding(
      padding: const EdgeInsets.symmetric(horizontal: 6, vertical: 12),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, size: 18, color: featureMuted),
          const SizedBox(height: 4),
          Text(label, style: const TextStyle(fontSize: 8, color: featureMuted)),
        ],
      ),
    ),
  );
  Widget _eventCard(BuildContext context, ArchiveEvent event) {
    final color = event.type == 'GROWTH_ANALYZED'
        ? const Color(0xFF72AF89)
        : event.type == 'LIFEMAP_CREATED'
        ? const Color(0xFFE6A366)
        : featurePurple;
    return FeatureCard(
      padding: 12,
      child: InkWell(
        onTap: () => showFeatureDetails(
          context,
          event.title,
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              FeatureTags([archiveTypes[event.type] ?? event.type]),
              const SizedBox(height: 12),
              Text(
                displayDate(event.date),
                style: const TextStyle(color: featureMuted, fontSize: 12),
              ),
              const SizedBox(height: 18),
              Text(
                event.summary ?? '저장된 요약이 없어요.',
                style: const TextStyle(height: 1.8),
              ),
              if (event.type == 'IDENTITY_CREATED')
                Padding(
                  padding: const EdgeInsets.only(top: 20),
                  child: FilledButton(
                    onPressed: () {
                      Navigator.pop(context);
                      context.push('/identity/${event.referenceId}');
                    },
                    child: const Text('Identity 기록 보기'),
                  ),
                ),
            ],
          ),
        ),
        child: Row(
          children: [
            CircleAvatar(
              radius: 20,
              backgroundColor: color.withValues(alpha: .1),
              child: Icon(
                event.type == 'GROWTH_ANALYZED'
                    ? Icons.spa_outlined
                    : event.type == 'LIFEMAP_CREATED'
                    ? Icons.hub_outlined
                    : event.type == 'OS_UPDATED'
                    ? Icons.psychology_outlined
                    : event.type == 'IDENTITY_CREATED'
                    ? Icons.person_outline
                    : Icons.description_outlined,
                size: 19,
                color: color,
              ),
            ),
            const SizedBox(width: 12),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    event.title,
                    style: const TextStyle(
                      fontSize: 12,
                      fontWeight: FontWeight.w700,
                    ),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    displayDate(event.date),
                    style: const TextStyle(fontSize: 9, color: featureMuted),
                  ),
                  if (event.summary != null)
                    Text(
                      event.summary!,
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
                      style: const TextStyle(
                        fontSize: 10,
                        height: 1.6,
                        color: featureMuted,
                      ),
                    ),
                ],
              ),
            ),
            const Icon(Icons.chevron_right, size: 18, color: featureMuted),
          ],
        ),
      ),
    );
  }
}
