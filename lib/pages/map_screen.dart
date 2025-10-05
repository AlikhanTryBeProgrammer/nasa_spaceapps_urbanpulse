import 'package:flutter/material.dart';
import 'package:webview_flutter/webview_flutter.dart';

class MapScreen extends StatefulWidget {
  const MapScreen({super.key});

  @override
  State<MapScreen> createState() => _MapScreenState();
}

class _MapScreenState extends State<MapScreen> {
  late final WebViewController _controller;

  @override
  void initState() {
    super.initState();
    _controller = WebViewController()
      ..setJavaScriptMode(JavaScriptMode.unrestricted)
      ..loadRequest(
        Uri.parse(
          // 🌍 сюда можно подставить ссылку на твою GEE-карту
          'https://earthengine.google.com/iframes/map/#v=43.25,76.9,8z',
        ),
      );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('GEE Map Viewer'),
        backgroundColor: const Color(0xFFE64A19),
      ),
      body: WebViewWidget(controller: _controller),
    );
  }
}
