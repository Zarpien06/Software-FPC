import 'package:flutter/material.dart';

class AuthService extends ChangeNotifier {
  // Usuario simulado
  String? _usuario;

  // Getter para saber si hay sesión iniciada
  bool get isAuthenticated => _usuario != null;

  // Obtener nombre de usuario actual
  String? get usuario => _usuario;

  // Login simulado
  Future<bool> login(String email, String password) async {
    await Future.delayed(const Duration(seconds: 1)); // Simula espera del backend

    // Puedes cambiar esto por una validación real
    if (email == 'admin@demo.com' && password == '123456') {
      _usuario = email;
      notifyListeners();
      return true;
    } else {
      return false;
    }
  }

  // Registro simulado
  Future<bool> register(String email, String password) async {
    await Future.delayed(const Duration(seconds: 1)); // Simula espera
    _usuario = email;
    notifyListeners();
    return true;
  }

  // Cerrar sesión
  void logout() {
    _usuario = null;
    notifyListeners();
  }
}
