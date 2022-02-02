import 'dart:typed_data';

import 'package:audioplayers/audioplayers.dart';

class Audio {
  Future<void> playByteStream({required Uint8List bytesList}) async {
    AudioPlayer audioPlayer = AudioPlayer();
    try {
      int result = await audioPlayer.playBytes(bytesList);
      print(result);
    } catch (e) {
      print(e);
    }
  }
}
