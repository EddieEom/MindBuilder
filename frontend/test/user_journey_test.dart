import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:frontend/app/app.dart';
import 'package:frontend/core/storage/token_storage.dart';
import 'package:frontend/features/settings/application/settings_controller.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  testWidgets('first launch can skip splash and reaches login', (tester) async {
    FlutterSecureStorage.setMockInitialValues({});
    await tester.pumpWidget(
      ProviderScope(
        overrides: [
          settingsProvider.overrideWith(
            (ref) => SettingsController(
              TokenStorage.instance,
              loadStoredValues: false,
            ),
          ),
        ],
        child: const MindBuilderApp(isLoggedIn: false),
      ),
    );
    await tester.pump();
    expect(find.text('건너뛰기'), findsOneWidget);
    await tester.tap(find.text('건너뛰기'));
    await tester.pumpAndSettle();
    expect(find.text('Google로 계속하기'), findsOneWidget);
    expect(find.text('Kakao로 계속하기'), findsOneWidget);
    expect(tester.takeException(), isNull);
  });
}
