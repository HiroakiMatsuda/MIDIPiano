MIDIPiano
======================
MIDIPianoはMIDI::Message型のデータを受けてソフトウェアシンセサイザを制御する[RT-Component][rtm]です．  
[おーぷんMIDIぷろじぇくと][openmidi]で配布されている[MIDIIOライブラリ][midiio]を通して，ソフトウェアシンセサイザを制御することができます．  
MIDI::Messageについては[こちら][idl]をごらんください． 

[rtm]:http://www.openrtm.org/openrtm/ja
[openmidi]: http://openmidiproject.sourceforge.jp/  
[midiio]: http://openmidiproject.sourceforge.jp/MIDIIOLibrary.html  
[idl]: https://github.com/HiroakiMatsuda/MIDIDataType

動作確認環境
------
Python:  
2.6.6  

OS:  
Windows 8/8.1 64bit / 32bit  

依存モジュール:  
[pymidiio][py-midiio]  

[py-midiio]:https://github.com/HiroakiMatsuda/pymidiio/

更新履歴:  
------

ファイル構成
------
MIDIPiano  
│― idl   
│― MIDI  
│― MIDI\_POA  
│― MIDIDataType\_idl.py  
│― pymidiio  
│  　　　│―\_\_init\_\_.py  
│  　　　│―midi\_out.py  
│  　　　│―midi\_structure.py  
│  　　　│―MIDIIO.dll(本DLLは付属していません)  
│― pyrs.py  
│― MIDIPiano.conf  
│― MIDIPiano.py  

* MIDI, MIDI_POA, MIDIDataType.py  
独自データ型 MIDIDataTypeに関するファイルです．  
 
* [pymidio][py-midiio]  
pymidiioは[おーぷんMIDIぷろじぇくと][openmidi]で配布されている[MIDIIOライブラリ][midiio]をPythonから使用するためのラッパーモジュールです．   
詳しくは，[ここ][py-midiio]をご覧ください．  

* MIDIPaino.conf  
ソフトウェアシンセサイザの音色やチャンネル番号の指定をコンフィグレーションで行うことがでいます．    

* MIDIPiano.py  
MIDIPiano RTC本体です．  

＊ 本RTCにおいてユーザーが操作すると想定しているファイルのみ説明しています．  

RTCの構成
------  
<img src="https://farm9.staticflickr.com/8650/15988383542_26c3046eed_o.png" width="400px" />    
データポートは1つあり、以下のようになっています  
  
* midi\_in port :InPort  
データ型; MIDI::MIDIMessage  
MIDIメッセージを受け取り，受け取ったデータに基づきソフトウェアシンセサイザを制御します．  

* コンフィグレーション  
 ・`channel`:  
 MIDIメッセージのチャンネルを設定します．  
 -1を設定した場合は，全チャンネルのメッセージに対して処理を行います．  
 ・`tone`:  
 ソフトウェアシンセサイザいの音色を設定します．  
 -1を設定した場合は，全チャンネルのメッセージに対して処理を行います．  
 ・`delay_time`:  
 各RTC間でMIDIメッセージの遅延をキャンセルための待ち時間を設定します．  
 設置は1/1000秒となります．  
 ・`device_name`:  
 使用するソフトウェアシンセサイザの名前を指定します．  
 
 コンフィグレーションはonStartUpで読み込みます．  
 モードを変更する場合は，一度MIDIPianoを終了し，コンフィグレーション変更後に再度実行して下さい．


使い方：　MIDIParserを使用してテストする
------
###1. MIDIIOライブラリを配置する###
まずは，MIDIIOライブラリを[おーぷんMIDIぷろじぇくとの配布ページ][midiio]よりMIDIIOライブラリ1.0(MIDIIOLib1.0.zip)をダウンロードしてください．  
ダウンロードしたMIDIOLib1.0.zipを適当な場所に解凍します．  
次に，MIDIIOLib1.0\Release\に格納されているMIDIO.dllをコピーします．  
コピーしたMIDIO.dllを本GitHubから入手したMIDIPianoフォルダ内にあるpymidiioフォルダの直下に配置してください．  
DLLファイルを配置した後の，pymidioフォルダのファイル構成は以下のようになります．  

pymidiio  
│― \_\_init\_\_.py     
│― midi\_out.py    
│― midi\_structure.py    
│― MIDIIO.dll  

###2. MIDIParserの入手する###
[MIDIParser][parser]はMIDIファイルを解析し，MIDI::MIDIMessage型のデータを曲のタイミングに合わせて出力するRTCです．  
[こちら][parser]よりDLしてください．  
Microsoft GS Wavetable Synth以外のソフトウェアシンセサイザを使用する場合は，MIDIPaino.conf内のdevice_nameを変更してください．  

[parser]:https://github.com/HiroakiMatsuda/MIDIParser

###3. 解析するMIDIファイルを設定する###
MIDIParser RTCに解析させるMIDIファイルを設定します．  

MIDIParser.confをテキストエディタなどで開きます．  
以下のようにコンフィグレーションが設定されていると思います．  

```conf.mode0.midi_file: ./midifile/simpletest.mid ```     

以下のように，mode numberとfile nameを設定することで複数MIDIファイルを登録することができます．  
＊MIDIファイルはmidifileフォルダ内に配置することを前提としています．  

```conf.mode<mode number>.midi_file: ./midifile/<file name>.mid ```     

###4. MIDIメセージを受け取る###
MIDIParser RTCとMIDIPiano RTCを実行してください．  
各RTCが起動したらMIDIParser RTCのmidi\_outポートとMIDIPiano RTCのmidi\_inポートを接続します．  
各ポートを接続したらMIDIParser RTCをActivateします．  
するとNote Onのイベントに合わせてピアノ音が演奏されます．  
      
以上が本RTCの使い方となります  

ライセンス
----------
Copyright &copy; 2014 Hiroaki Matsuda  
Licensed under the [Apache License, Version 2.0][Apache]  
Distributed under the [MIT License][mit].  
Dual licensed under the [MIT license][MIT] and [GPL license][GPL].  
 
[Apache]: http://www.apache.org/licenses/LICENSE-2.0
[MIT]: http://www.opensource.org/licenses/mit-license.php
[GPL]: http://www.gnu.org/licenses/gpl.html