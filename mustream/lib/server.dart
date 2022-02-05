import 'dart:io';
import 'dart:typed_data';
import 'package:mustream/audio.dart';

class Server {
  Future<void> initiate() async {
    final server =
        await ServerSocket.bind(InternetAddress.anyIPv4, 5902, shared: true);

    print("Server Started");

    server.listen((client) {
      handleConnection(client);
    });
  }

  void handleConnection(Socket client) async {
    print('Connection from'
        ' ${client.remoteAddress.address}:${client.remotePort}');

    var bytesBuilder = BytesBuilder();
    Audio audio = Audio();
    await audio.setPlayer();

    // listen for events from the client
    client.listen(
      (Uint8List data) async {
        bytesBuilder.add(data);

        if (bytesBuilder.length == 14380) {
          print("Recieved packet");
          audio.playByteStream(bytesList: bytesBuilder.takeBytes());
        }
      },

      // handle errors
      onError: (error) {
        print(error);
        client.close();
      },

      // handle the client closing the connection
      onDone: () async {
        print('Client left');
        client.close();
      },
    );
  }
}
