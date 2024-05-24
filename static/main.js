// //ドロップダウンの設定を関数でまとめる
// function mediaQueriesWin(){
//   var width = $(window).width();
//   if(width <= 768) {//横幅が768px以下の場合
//     $(".dropdownlink>a").off('click'); //has-childクラスがついたaタグのonイベントを複数登録を避ける為offにして一旦初期状態へ
//     $(".dropdownlink>a").on('click', function() {//has-childクラスがついたaタグをクリックしたら
//       var parentElem =  $(this).parent();// aタグから見た親要素の<li>を取得し
//       $(parentElem).toggleClass('active');//矢印方向を変えるためのクラス名を付与して
//       $(parentElem).children('ul').stop().slideToggle(500);//liの子要素のスライドを開閉させる※数字が大きくなるほどゆっくり開く
//       return false;//リンクの無効化
//     });
//   }else{//横幅が768px以上の場合
//     $(".dropdownlink>a").off('click');//has-childクラスがついたaタグのonイベントをoff(無効)にし
//     $(".dropdownlink").removeClass('active');//activeクラスを削除
//     $('.dropdownlink').children('ul').css("display","");//スライドトグルで動作したdisplayも無効化にする
//   }
// }
//
// // ページがリサイズされたら動かしたい場合の記述
// $(window).resize(function() {
//   mediaQueriesWin();/* ドロップダウンの関数を呼ぶ*/
// });
//
// // ページが読み込まれたらすぐに動かしたい場合の記述
// $(window).on('load',function(){
//   mediaQueriesWin();/* ドロップダウンの関数を呼ぶ*/
// });


  document.addEventListener("DOMContentLoaded", function() {
  var mainSelect = document.querySelector('.main_select');
  var subSelects = document.querySelectorAll('.sub_select');

  subSelects.forEach(select => select.style.display = 'none');

  mainSelect.addEventListener('change', function() {
  subSelects.forEach(select => {
  select.style.display = 'none';
  select.required = false;
});

  var selectedGroup = mainSelect.value;
  if (selectedGroup) {
  var targetSelect = document.getElementById(selectedGroup);
  if (targetSelect) {
  targetSelect.style.display = 'inline-block';
  targetSelect.required = true;
}
}
});
});
