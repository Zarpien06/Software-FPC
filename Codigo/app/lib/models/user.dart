class UserModel {
  final String email;
  final String name;

  UserModel({
    required this.email,
    required this.name,
  });

  // Crear usuario desde un mapa (ideal si luego usas JSON de un backend)
  factory UserModel.fromMap(Map<String, dynamic> data) {
    return UserModel(
      email: data['email'] ?? '',
      name: data['name'] ?? '',
    );
  }

  // Convertir a mapa (ideal para enviar al backend)
  Map<String, dynamic> toMap() {
    return {
      'email': email,
      'name': name,
    };
  }
}
