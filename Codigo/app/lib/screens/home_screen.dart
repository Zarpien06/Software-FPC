import 'package:flutter/material.dart';

class HomeScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Bienvenido'),
        actions: [
          IconButton(
            icon: Icon(Icons.logout),
            onPressed: () =>
                Navigator.pushReplacementNamed(context, '/login'),
          ),
        ],
      ),
      body: Center(
        child: Text(
          '¡Has iniciado sesión exitosamente!',
          style: TextStyle(fontSize: 20),
        ),
      ),
    );
  }
}
