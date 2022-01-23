import 'package:flutter/material.dart';
import 'package:mustream_mobile/services/server.dart';

class HomePage extends StatefulWidget {
  HomePage({Key? key}) : super(key: key);

  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Mustream'),
      ),
      body: Center(
        child: ElevatedButton(
          onPressed: () {
            var s = Server();
            s.initiate(port: 4444);
          },
          child: const Text('Turn ON'),
        ),
      ),
    );
  }
}
