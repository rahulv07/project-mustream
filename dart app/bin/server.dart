import 'dart:io';
import 'dart:typed_data';
import 'dart:collection';

import 'audio.dart';

void main() async {
  final server = await ServerSocket.bind(InternetAddress.anyIPv4, 5902);

  print("Server Started");

  server.listen((client) {
    handleConnection(client);
  });
}

void handleConnection(Socket client) {
  print('Connection from'
      ' ${client.remoteAddress.address}:${client.remotePort}');
  int packetNo = 0;
  // listen for events from the client
  client.listen(
    (Uint8List data) async {
      print(data.sublist(0, 11));
    },

    // handle errors
    onError: (error) {
      print(error);
      client.close();
    },

    // handle the client closing the connection
    onDone: () {
      client.close();
    },
  );
}
