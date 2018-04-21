import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

void main() {
  runApp(new MaterialApp(
    home: new MyApp(),
  ));
}

class MyApp extends StatefulWidget {
  @override
  _State createState() => new _State();
}

class _State extends State<MyApp> {
  String _text = '';

  double _speed = 0.0;
  int _brightness = 100; //btwn 0 & 100

  void _setSpeed(double speed) =>
      setState(() => _speed = (speed * 100).round() / 100);
  void _setBrightness(double brightness) =>
      setState(() => _brightness = brightness.round());

  void _onChange(String text) {
    setState(() => _text = text);
  }

  void _onSubmit() {
    print('huhu');

    String url = "http://192.168.1.139";
    http.post(url, body: {"text": _text, "speed": _speed.toString(), "brightness": _brightness.toString()}).then((response) {
      print("Response status: ${response.statusCode}");
      print("Response body: ${response.body}");
    });
  }

  @override
  Widget build(BuildContext context) {
    return new Scaffold(
      appBar: new AppBar(
        title: new Text('Anzeige App'),
      ),
      body: new Container(
          padding: new EdgeInsets.all(32.0),
          child: new Center(
            child: new Column(
              children: <Widget>[
                new TextField(
                  decoration: new InputDecoration(
                      labelText: 'Text auf der Anzeige',
                      hintText: 'Welcher Text soll auf der Anzeige stehen?',
                      icon: new Icon(Icons.subtitles)),
                  autocorrect: true,
                  autofocus: true,
                  keyboardType: TextInputType.text,
                  onChanged: _onChange,
                ),
                new Text('Laufgeschwindingkeit: ${_speed}'),
                new Slider(
                  value: _speed,
                  onChanged: _setSpeed,
                  min: 0.0,
                  max: 2.0,
                ),
                new Text('Helligkeit: ${_brightness}'),
                new Slider(
                  value: _brightness * 1.0,
                  onChanged: _setBrightness,
                  min: 0.0,
                  max: 100.0,
                ),
                new IconButton(
                  onPressed: _onSubmit,
                  icon: new Icon(Icons.send),
                ),
              ],
            ),
          )),
    );
  }
}
