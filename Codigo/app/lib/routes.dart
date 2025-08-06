import 'package:flutter/material.dart';
import 'screens/home_screen.dart';
import 'screens/login_screen.dart';
import 'screens/register_screen.dart';
import 'screens/dashboard_screen.dart';

final Map<String, WidgetBuilder> appRoutes = {
  '/': (_) => HomeScreen(),
  '/login': (_) => LoginScreen(),
  '/register': (_) => RegisterScreen(),
  '/dashboard': (_) => DashboardScreen(),
};
