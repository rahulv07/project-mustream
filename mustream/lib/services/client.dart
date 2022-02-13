import 'dart:io';
import 'dart:typed_data';
import 'audio.dart';

class Client {
  Future<void> connect(ipAddr, port) async {
    final socket = await Socket.connect(ipAddr, port);
    print('Connected to: ${socket.remoteAddress.address}:${socket.remotePort}');

    var bytesBuilder = BytesBuilder();
    int i = 0;
    Audio audio = Audio();
    await audio.setPlayer();

    // listen for events from the client
    socket.listen(
      (Uint8List data) async {
        bytesBuilder.add(data);

        if (bytesBuilder.length == 86060) {
          i++;
          socket.write("ACK");
          audio.playByteStream(bytesList: bytesBuilder.takeBytes());
        }
      },

      // handle errors
      onError: (error) {
        print(error);
        socket.close();
      },

      // handle the client closing the connection
      onDone: () async {
        print('Done');
        socket.close();
        print("Total packets received $i");
      },
    );
  }
}
