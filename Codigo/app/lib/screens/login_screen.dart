import 'package:flutter/material.dart';

class LoginScreen extends StatefulWidget {
  @override
  _LoginScreenState createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _formKey = GlobalKey<FormState>();

  String _email = '';
  String _password = '';
  bool _isLoading = false;

  void _submitLogin() {
    if (_formKey.currentState!.validate()) {
      _formKey.currentState!.save();
      setState(() => _isLoading = true);

      // Simulación de autenticación
      Future.delayed(Duration(seconds: 2), () {
        setState(() => _isLoading = false);
        if (_email == 'usuario@email.com' && _password == '123456') {
          Navigator.pushReplacementNamed(context, '/home');
        } else {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(content: Text('Correo o contraseña incorrectos')),
          );
        }
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Iniciar Sesión')),
      body: Center(
        child: SingleChildScrollView(
          padding: EdgeInsets.symmetric(horizontal: 24.0),
          child: Form(
            key: _formKey,
            child: Column(
              children: [
                Icon(Icons.lock_outline, size: 80, color: Colors.indigo),
                SizedBox(height: 20),
                TextFormField(
                  decoration: InputDecoration(labelText: 'Correo electrónico'),
                  keyboardType: TextInputType.emailAddress,
                  onSaved: (value) => _email = value!,
                  validator: (value) =>
                      value!.contains('@') ? null : 'Correo no válido',
                ),
                TextFormField(
                  decoration: InputDecoration(labelText: 'Contraseña'),
                  obscureText: true,
                  onSaved: (value) => _password = value!,
                  validator: (value) =>
                      value!.length < 6 ? 'Mínimo 6 caracteres' : null,
                ),
                SizedBox(height: 20),
                _isLoading
                    ? CircularProgressIndicator()
                    : ElevatedButton(
                        onPressed: _submitLogin,
                        child: Text('Iniciar Sesión'),
                      ),
                TextButton(
                  onPressed: () =>
                      Navigator.pushReplacementNamed(context, '/register'),
                  child: Text('¿No tienes cuenta? Regístrate'),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
