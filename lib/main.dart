import 'package:flutter/material.dart';
import 'pages/home_screen.dart';

void main() {
  runApp(const UrbanPulseApp());
}

class UrbanPulseApp extends StatelessWidget {
  const UrbanPulseApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: "UrbanPulse",
      theme: ThemeData(
        primaryColor: const Color(0xFF1F2C46),
        scaffoldBackgroundColor: Colors.white,
        useMaterial3: true,
      ),
      home: const WelcomeScreen(),
    );
  }
}

class WelcomeScreen extends StatelessWidget {
  const WelcomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      body: SafeArea(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            const SizedBox(height: 40),

            // Заголовок
            const Text(
              "Welcome\nto UrbanPulse",
              textAlign: TextAlign.center,
              style: TextStyle(
                fontSize: 28,
                fontWeight: FontWeight.bold,
                color: Color(0xFF1F2C46),
              ),
            ),

            // Иллюстрация с двумя маленькими картинками
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 20),
              child: Stack(
                alignment: Alignment.center,
                children: [
                  // Основная картинка
                  Image.asset(
                    "assets/data/mainscreen.png",
                    height: 280,
                    fit: BoxFit.contain,
                  ),

                  // Картинка слева сверху
                  Positioned(
                    top: 10,
                    left: 10,
                    child: Image.asset(
                      "assets/data/frame1.png",
                      width: 70,
                      height: 70,
                    ),
                  ),

                  // Картинка справа сверху
                  Positioned(
                    top: 10,
                    right: 10,
                    child: Image.asset(
                      "assets/data/frame2.png",
                      width: 70,
                      height: 70,
                    ),
                  ),
                ],
              ),
            ),

            // Кнопка Get Started
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 24),
              child: SizedBox(
                width: double.infinity,
                child: ElevatedButton.icon(
                  onPressed: () {
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (context) => const HomeScreen(),
                      ),
                    );
                  },
                  icon: const Icon(Icons.home_outlined, color: Colors.white),
                  label: const Text(
                    "Get Started",
                    style: TextStyle(fontSize: 18, fontWeight: FontWeight.w600),
                  ),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: const Color(0xFF1F2C46),
                    padding: const EdgeInsets.symmetric(vertical: 14),
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(12),
                    ),
                  ),
                ),
              ),
            ),

            // Sign In
            Padding(
              padding: const EdgeInsets.only(bottom: 20, top: 12),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const Text(
                    "Already have an account? ",
                    style: TextStyle(fontSize: 14, color: Colors.black87),
                  ),
                  GestureDetector(
                    onTap: () {
                      ScaffoldMessenger.of(context).showSnackBar(
                        const SnackBar(
                          content: Text("Sign In feature coming soon"),
                        ),
                      );
                    },
                    child: const Text(
                      "Sign In",
                      style: TextStyle(
                        fontSize: 14,
                        fontWeight: FontWeight.bold,
                        color: Color(0xFF1F2C46),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
