import 'package:flutter/material.dart';
import '../services/bot_service.dart';

class BotResultScreen extends StatefulWidget {
  const BotResultScreen({super.key});

  @override
  State<BotResultScreen> createState() => _BotResultScreenState();
}

class _BotResultScreenState extends State<BotResultScreen> {
  final TextEditingController _controller = TextEditingController();
  List<Map<String, dynamic>> _results = [];
  bool _loading = false;

  void _analyze() async {
    final text = _controller.text.trim();
    if (text.isEmpty) return;

    setState(() => _loading = true);

    try {
      int month = int.tryParse(text) ?? 0;
      final res = await fetchBotAnalysis(month);
      setState(() => _results = res);
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text("Ошибка соединения с Flask API")),
      );
    }

    setState(() => _loading = false);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("AI Assistant (Python Bot)"),
        backgroundColor: const Color(0xFF5D4037),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _controller,
                    decoration: const InputDecoration(
                      hintText: "Введите номер месяца (1–12)",
                      border: OutlineInputBorder(),
                    ),
                  ),
                ),
                const SizedBox(width: 8),
                ElevatedButton(
                  onPressed: _analyze,
                  style: ElevatedButton.styleFrom(
                    backgroundColor: const Color(0xFF5D4037),
                  ),
                  child: const Text("Анализ"),
                ),
              ],
            ),
            const SizedBox(height: 20),
            if (_loading) const LinearProgressIndicator(),
            Expanded(
              child: _results.isEmpty
                  ? const Center(
                      child: Text("Введите месяц и нажмите 'Анализ'"),
                    )
                  : ListView.builder(
                      itemCount: _results.length,
                      itemBuilder: (context, i) {
                        final r = _results[i];
                        final city = r["city"];
                        final temp = r["temp_surface"];
                        final pm = r["pm25"];
                        final health = r["health_index"];
                        final recs = List.from(r["recommendations"] ?? []);
                        return Card(
                          color: const Color(0xFFFFF8E1),
                          margin: const EdgeInsets.symmetric(vertical: 8),
                          child: Padding(
                            padding: const EdgeInsets.all(12.0),
                            child: Column(
                              crossAxisAlignment: CrossAxisAlignment.start,
                              children: [
                                Text(
                                  "🏙 $city",
                                  style: const TextStyle(
                                    fontSize: 18,
                                    fontWeight: FontWeight.bold,
                                  ),
                                ),
                                const SizedBox(height: 4),
                                Text("🌡 Температура: $temp °C"),
                                Text("💨 PM2.5: $pm µg/m³"),
                                Text(
                                  "❤️ Health Index: ${health.toStringAsFixed(2)}",
                                ),
                                const SizedBox(height: 6),
                                const Text(
                                  "Рекомендации:",
                                  style: TextStyle(fontWeight: FontWeight.w600),
                                ),
                                for (var r in recs)
                                  Text(
                                    "• $r",
                                    style: const TextStyle(
                                      color: Colors.black87,
                                    ),
                                  ),
                              ],
                            ),
                          ),
                        );
                      },
                    ),
            ),
          ],
        ),
      ),
    );
  }
}
