import 'dart:io';
import 'dart:typed_data';

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

  // listen for events from the client
  client.listen(
    (Uint8List data) async {
      await Future.delayed(Duration(seconds: 1));
      print(data.length);
    },

    // handle errors
    onError: (error) {
      print(error);
      client.close();
    },

    // handle the client closing the connection
    onDone: () {
      print('Client left');
      client.close();
    },
  );
}
