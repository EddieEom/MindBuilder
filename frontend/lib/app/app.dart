import 'package:flutter/material.dart';

import '../core/routes/app_router.dart';
import '../core/theme/app_theme.dart';

class MindBuilderApp extends StatelessWidget {
  const MindBuilderApp({
    super.key,
    required this.isLoggedIn,
  });

  final bool isLoggedIn;

  @override
  Widget build(BuildContext context) {
    return MaterialApp.router(
      title: 'MindBuilder',
      debugShowCheckedModeBanner: false,

      theme: AppTheme.lightTheme,

      routerConfig: AppRouter.createRouter(
        isLoggedIn: isLoggedIn,
      ),
    );
  }
}