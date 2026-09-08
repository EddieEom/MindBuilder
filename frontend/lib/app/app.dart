import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../core/routes/app_router.dart';
import '../core/theme/app_theme.dart';
import '../features/settings/application/settings_controller.dart';

class MindBuilderApp extends ConsumerStatefulWidget {
  const MindBuilderApp({super.key, required this.isLoggedIn});

  final bool isLoggedIn;

  @override
  ConsumerState<MindBuilderApp> createState() => _MindBuilderAppState();
}

class _MindBuilderAppState extends ConsumerState<MindBuilderApp> {
  late final GoRouter _router;

  @override
  void initState() {
    super.initState();
    _router = AppRouter.createRouter(isLoggedIn: widget.isLoggedIn);
  }

  @override
  Widget build(BuildContext context) {
    final settings = ref.watch(settingsProvider);
    return MaterialApp.router(
      title: 'MindBuilder',
      debugShowCheckedModeBanner: false,

      theme: AppTheme.lightTheme,
      darkTheme: AppTheme.darkTheme,
      themeMode: settings.darkMode ? ThemeMode.dark : ThemeMode.light,
      routerConfig: _router,
    );
  }
}
