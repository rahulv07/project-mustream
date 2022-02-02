import 'dart:io';
import 'dart:typed_data';
import 'package:mustream/audio.dart';

class Server {
  var bytesBuilder = BytesBuilder();
  Future<void> initiate() async {
    final server =
        await ServerSocket.bind(InternetAddress.anyIPv4, 5902, shared: true);

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
        print(data.length);
        bytesBuilder.add(data);
      },

      // handle errors
      onError: (error) {
        print(error);
        client.close();
      },

      // handle the client closing the connection
      onDone: () async {
        print('Client left');
        var receivedData = bytesBuilder.toBytes();
        print("Total received bytes: ${receivedData.length}");
        client.close();
        print("Playing audio...");
        Audio audio = Audio();
        await audio.playByteStream(bytesList: receivedData);
      },
    );
  }
}
