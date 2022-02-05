//Imitates the Audio Class in the mustream mobile application

class Audio {
  Future<bool> playBytesStream({bytesList}) async {
    int result = await Future.delayed(Duration(seconds: 1)).then((value) {
      return 1;
    });

    if (result == 1)
      return true;
    else
      return false;
  }
}
