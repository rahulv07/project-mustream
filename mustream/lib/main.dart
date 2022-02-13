import 'package:flutter/material.dart';
import 'services/client.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: HomePage(),
    );
  }
}

class HomePage extends StatelessWidget {
  HomePage({Key? key}) : super(key: key);

  String ipAddress = '';
  int port = 5902;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
          child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Padding(
            padding: const EdgeInsets.all(30),
            child: TextField(
              autofocus: true,
              cursorColor: Colors.black,
              cursorHeight: 30.0,
              decoration: const InputDecoration(
                hintText: "IP address",
                hintStyle: TextStyle(color: Colors.grey),
                enabledBorder: UnderlineInputBorder(
                  borderSide: BorderSide(
                    color: Colors.red,
                  ),
                ),
                focusedBorder: UnderlineInputBorder(
                  borderSide: BorderSide(
                    color: Colors.blue,
                  ),
                ),
              ),
              style: const TextStyle(
                color: Colors.black,
                fontSize: 20.0,
              ),
              onChanged: (text) {
                ipAddress = text;
              },
            ),
          ),
          const SizedBox(height: 25),
          ElevatedButton(
            onPressed: () async {
              print('Client pressed.');
              Client client = Client();
              await client.connect(ipAddress, port);
            },
            child: const Text('Connect'),
          ),
        ],
      )),
    );
  }
}
