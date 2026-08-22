import 'package:flutter/material.dart';

abstract final class AppColors {
  // =========================
  // Primary
  // =========================

  static const Color primary = Color(0xFF635BCE);
  static const Color primaryLight = Color(0xFF8B84E8);
  static const Color primaryDark = Color(0xFF4C45A8);

  // =========================
  // Background
  // =========================

  static const Color background = Color(0xFFF7F8FC);
  static const Color backgroundSoft = Color(0xFFF1F3FA);

  // =========================
  // Surface
  // =========================

  static const Color surface = Color(0xFFFFFFFF);
  static const Color surfaceSecondary = Color(0xFFF8F9FD);

  // =========================
  // Text
  // =========================

  static const Color textPrimary = Color(0xFF1F2340);
  static const Color textSecondary = Color(0xFF6E7287);
  static const Color textTertiary = Color(0xFFA5A8B8);
  static const Color textOnPrimary = Color(0xFFFFFFFF);

  // =========================
  // Border / Divider
  // =========================

  static const Color border = Color(0xFFE4E6F0);
  static const Color divider = Color(0xFFEEF0F6);

  // =========================
  // Semantic Colors
  // =========================

  // Growth / Positive
  static const Color success = Color(0xFF65BFA8);
  static const Color successLight = Color(0xFFEAF7F2);

  // Insight / Highlight
  static const Color accentPink = Color(0xFFEFA4B6);
  static const Color accentPinkLight = Color(0xFFFFF0F4);

  // Information
  static const Color info = Color(0xFF6D8EEB);
  static const Color infoLight = Color(0xFFEEF2FF);

  // Warning
  static const Color warning = Color(0xFFF0B76A);
  static const Color warningLight = Color(0xFFFFF6E8);

  // Error
  static const Color error = Color(0xFFE57373);
  static const Color errorLight = Color(0xFFFFEEEE);
}