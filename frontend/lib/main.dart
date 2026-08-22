import 'package:flutter/material.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'app/app.dart';
import 'core/storage/token_storage.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  await dotenv.load();

  // await TokenStorage.instance.clearTokens();

  final accessToken =
      await TokenStorage.instance.getAccessToken();

  final bool isLoggedIn =
      accessToken != null && accessToken.isNotEmpty;

  runApp(
    ProviderScope(
      child: MindBuilderApp(
        isLoggedIn: isLoggedIn,
      ),
    ),
  );
}