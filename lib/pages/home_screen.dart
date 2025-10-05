import 'package:flutter/material.dart';
import 'map_screen.dart';
import 'bot_result_screen.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Верхняя строка
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  const Text(
                    "User",
                    style: TextStyle(fontSize: 18, fontWeight: FontWeight.w500),
                  ),
                  Row(
                    children: [
                      _circleIcon(Icons.notifications_outlined),
                      const SizedBox(width: 10),
                      _circleIcon(Icons.settings_outlined),
                    ],
                  ),
                ],
              ),
              const SizedBox(height: 20),

              // Поисковая строка
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 12),
                decoration: BoxDecoration(
                  color: const Color(0xFFFFF59D),
                  borderRadius: BorderRadius.circular(20),
                ),
                child: Row(
                  children: const [
                    Expanded(
                      child: TextField(
                        decoration: InputDecoration(
                          hintText: "Search Location...",
                          border: InputBorder.none,
                        ),
                      ),
                    ),
                    Icon(Icons.search, color: Colors.black54),
                  ],
                ),
              ),
              const SizedBox(height: 20),

              // Локация
              const Text(
                "My Location:",
                style: TextStyle(
                  fontSize: 22,
                  fontWeight: FontWeight.bold,
                  color: Color(0xFF1F2C46),
                ),
              ),
              const SizedBox(height: 8),
              Container(
                padding: const EdgeInsets.symmetric(
                  horizontal: 16,
                  vertical: 10,
                ),
                decoration: BoxDecoration(
                  color: const Color(0xFFFFF59D),
                  borderRadius: BorderRadius.circular(20),
                ),
                child: const Text(
                  "Almaty, Kazakhstan",
                  style: TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.w600,
                    color: Colors.black87,
                  ),
                ),
              ),
              const SizedBox(height: 20),

              // Карточки
              Expanded(
                child: ListView(
                  children: [
                    _featureCard(
                      title: "AI Assistant",
                      color: const Color(0xFF5D4037),
                      image: "assets/data/bot2.png",
                      onTap: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (context) => const BotResultScreen(),
                          ),
                        );
                      },
                    ),

                    const SizedBox(height: 16),

                    // 🚀 NASA Data Map с двумя дополнительными изображениями
                    _featureCard(
                      title: "NASA Data Map",
                      color: const Color(0xFFE64A19),
                      image: "assets/data/rocket2.png",
                      onTap: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (context) => const MapScreen(),
                          ),
                        );
                      },
                      extraImages: const [
                        Positioned(
                          right: 0,
                          top: 0,
                          child: Image(
                            image: AssetImage("assets/data/nearrocket2.png"),
                            width: 30,
                            height: 30,
                          ),
                        ),
                        Positioned(
                          left: 0,
                          bottom: 0,
                          child: Image(
                            image: AssetImage("assets/data/nearrocket1.png"),
                            width: 30,
                            height: 30,
                          ),
                        ),
                      ],
                    ),

                    const SizedBox(height: 16),

                    _featureCard(
                      title: "More Resources",
                      color: const Color(0xFF8BC34A),
                      image: "assets/data/comp.png",
                      onTap: () {
                        // Действия для будущих ресурсов
                      },
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  // Круглая иконка сверху
  Widget _circleIcon(IconData icon) {
    return Container(
      padding: const EdgeInsets.all(8),
      decoration: const BoxDecoration(
        color: Color(0xFFDCEDC8),
        shape: BoxShape.circle,
      ),
      child: Icon(icon, size: 22, color: Colors.black87),
    );
  }

  // Карточка с возможностью добавить дополнительные изображения
  Widget _featureCard({
    required String title,
    required Color color,
    required String image,
    VoidCallback? onTap,
    List<Widget>? extraImages, // 👈 добавлено для дополнительных картинок
  }) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        padding: const EdgeInsets.all(20),
        decoration: BoxDecoration(
          color: color,
          borderRadius: BorderRadius.circular(20),
        ),
        height: 120,
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(
              title,
              style: const TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
                color: Colors.white,
              ),
            ),
            Stack(
              clipBehavior: Clip.none,
              children: [
                Image.asset(image, height: 80, fit: BoxFit.contain),
                if (extraImages != null) ...extraImages,
              ],
            ),
          ],
        ),
      ),
    );
  }
}
