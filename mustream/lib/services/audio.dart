import 'dart:typed_data';
import 'package:audioplayers/audioplayers.dart';

class Audio {
  AudioPlayer audioPlayer = AudioPlayer();

  Future<void> setPlayer() async {
    await audioPlayer.setReleaseMode(ReleaseMode.STOP);
  }

  Future<void> playByteStream({required Uint8List bytesList}) async {
    try {
      int result = await audioPlayer.playBytes(bytesList);
      print(result);
    } catch (e) {
      print(e);
    }
  }
}
