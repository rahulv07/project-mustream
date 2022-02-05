import 'dart:typed_data';

import 'package:audioplayers/audioplayers.dart';

class Audio {
  AudioPlayer audioPlayer = AudioPlayer();
  Future<void> playByteStream({required Uint8List bytesList}) async {
    try {
      int result = await audioPlayer.playBytes(bytesList);
      print(result);
      //print("Duration: ${await audioPlayer.getDuration()}");
    } catch (e) {
      print(e);
    }
  }
}
