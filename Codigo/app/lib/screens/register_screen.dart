import 'package:flutter/material.dart';

class RegisterScreen extends StatefulWidget {
  @override
  _RegisterScreenState createState() => _RegisterScreenState();
}

class _RegisterScreenState extends State<RegisterScreen> {
  final _formKey = GlobalKey<FormState>();

  String _nombre = '';
  String _email = '';
  String _password = '';

  bool _isLoading = false;

  void _submitForm() {
    if (_formKey.currentState!.validate()) {
      _formKey.currentState!.save();
      setState(() => _isLoading = true);

      // Aquí iría la lógica para enviar datos al backend
      Future.delayed(Duration(seconds: 2), () {
        setState(() => _isLoading = false);
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Registro exitoso para $_nombre')),
        );
        Navigator.pushReplacementNamed(context, '/login');
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Registrarse')),
      body: Center(
        child: SingleChildScrollView(
          padding: EdgeInsets.symmetric(horizontal: 24.0),
          child: Form(
            key: _formKey,
            child: Column(
              children: [
                Icon(Icons.person_add, size: 80, color: Colors.indigo),
                SizedBox(height: 20),
                TextFormField(
                  decoration: InputDecoration(labelText: 'Nombre completo'),
                  onSaved: (value) => _nombre = value!,
                  validator: (value) =>
                      value!.isEmpty ? 'Por favor ingrese su nombre' : null,
                ),
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
                  validator: (value) => value!.length < 6
                      ? 'Mínimo 6 caracteres'
                      : null,
                ),
                SizedBox(height: 20),
                _isLoading
                    ? CircularProgressIndicator()
                    : ElevatedButton(
                        onPressed: _submitForm,
                        child: Text('Registrarse'),
                      ),
                TextButton(
                  onPressed: () =>
                      Navigator.pushReplacementNamed(context, '/login'),
                  child: Text('¿Ya tienes cuenta? Inicia sesión'),
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
