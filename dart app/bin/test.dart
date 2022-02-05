import 'dart:collection';

void main() async {
  Queue<int> queue = Queue();
  queue.addAll([1, 2, 3, 4, 5]);

  for (int i in queue) {
    await Future.delayed(Duration(seconds: 5));
    print(i);
    hi();
  }
}

void hi() {
  print("hi");
}
