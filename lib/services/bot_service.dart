import 'dart:convert';
import 'package:http/http.dart' as http;

/// Отправляет сообщение (месяц) к Flask API и получает ответ
Future<List<Map<String, dynamic>>> fetchBotAnalysis(int month) async {
  final url = Uri.parse('http://127.0.0.1:5000/analyze'); // Flask endpoint
  final response = await http.post(
    url,
    headers: {'Content-Type': 'application/json'},
    body: jsonEncode({'month': month}),
  );

  if (response.statusCode == 200) {
    final decoded = jsonDecode(response.body);
    return List<Map<String, dynamic>>.from(decoded['results'] ?? []);
  } else {
    throw Exception('Ошибка при подключении к Flask API');
  }
}
