import 'dart:io';
import 'dart:typed_data';

class Server {
  void initiate({required int port}) {
    print("Server Initiated...");
    ServerSocket.bind(InternetAddress.anyIPv4, port, shared: true)
        .then((ServerSocket server) {
      server.listen(_handleClient);
    });
  }

  void _handleClient(Socket client) {
    print('Connection from '
        '${client.remoteAddress.address}:${client.remotePort}');

    client.listen((Uint8List data) async {
      await Future.delayed(const Duration(seconds: 1));
      final message = String.fromCharCodes(data);
      print(message);
    }, onError: (error) {
      print(error);
      client.close();
    }, onDone: () {
      client.close();
    });
    //client.close();
  }
}
