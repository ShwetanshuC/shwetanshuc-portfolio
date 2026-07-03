// Created by iWeb 3.0.4 local-build-20260106

function createMediaStream_id5()
{return IWCreatePhotocast("http://www.millerpiano.com/Miller_Piano/Used_Grands_files/rss.xml",false);}
function initializeMediaStream_id5()
{createMediaStream_id5().load('http://www.millerpiano.com/Miller_Piano',function(imageStream)
{var entryCount=imageStream.length;var headerView=widgets['widget0'];headerView.setPreferenceForKey(imageStream.length,'entryCount');NotificationCenter.postNotification(new IWNotification('SetPage','id5',{pageIndex:0}));});}
function layoutMediaGrid_id5(range)
{createMediaStream_id5().load('http://www.millerpiano.com/Miller_Piano',function(imageStream)
{if(range==null)
{range=new IWRange(0,imageStream.length);}
IWLayoutPhotoGrid('id5',new IWPhotoGridLayout(3,new IWSize(158,158),new IWSize(158,48),new IWSize(238,221),27,27,0,new IWSize(14,14)),new IWPhotoFrame([IWCreateImage('Used_Grands_files/Hardcover_bevel_01.png'),IWCreateImage('Used_Grands_files/Hardcover_bevel_02.png'),IWCreateImage('Used_Grands_files/Hardcover_bevel_03.png'),IWCreateImage('Used_Grands_files/Hardcover_bevel_06.png'),IWCreateImage('Used_Grands_files/Hardcover_bevel_09.png'),IWCreateImage('Used_Grands_files/Hardcover_bevel_08.png'),IWCreateImage('Used_Grands_files/Hardcover_bevel_07.png'),IWCreateImage('Used_Grands_files/Hardcover_bevel_04.png')],null,0,0.400000,0.000000,0.000000,0.000000,0.000000,17.000000,17.000000,17.000000,17.000000,403.000000,295.000000,403.000000,295.000000,null,null,null,0.100000),imageStream,range,null,null,1.000000,null,'Media/slideshow.html','widget0','widget1','widget2')});}
function relayoutMediaGrid_id5(notification)
{var userInfo=notification.userInfo();var range=userInfo['range'];layoutMediaGrid_id5(range);}
setTransparentGifURL('Media/transparent.gif');function applyEffects()
{var registry=IWCreateEffectRegistry();registry.registerEffects({stroke_1:new IWStrokeParts([{rect:new IWRect(-1,1,2,30),url:'Used_Grands_files/stroke.png'},{rect:new IWRect(-1,-1,2,2),url:'Used_Grands_files/stroke_1.png'},{rect:new IWRect(1,-1,968,2),url:'Used_Grands_files/stroke_2.png'},{rect:new IWRect(969,-1,2,2),url:'Used_Grands_files/stroke_3.png'},{rect:new IWRect(969,1,2,30),url:'Used_Grands_files/stroke_4.png'},{rect:new IWRect(969,31,2,2),url:'Used_Grands_files/stroke_5.png'},{rect:new IWRect(1,31,968,2),url:'Used_Grands_files/stroke_6.png'},{rect:new IWRect(-1,31,2,2),url:'Used_Grands_files/stroke_7.png'}],new IWSize(970,32)),stroke_0:new IWEmptyStroke()});registry.applyEffects();}
function hostedOnDM()
{return false;}
function onPageLoad()
{IWRegisterNamedImage('comment overlay','Media/Photo-Overlay-Comment.png')
IWRegisterNamedImage('movie overlay','Media/Photo-Overlay-Movie.png')
loadMozillaCSS('Used_Grands_files/Used_GrandsMoz.css')
adjustLineHeightIfTooBig('id1');adjustFontSizeIfTooBig('id1');adjustLineHeightIfTooBig('id2');adjustFontSizeIfTooBig('id2');adjustLineHeightIfTooBig('id3');adjustFontSizeIfTooBig('id3');adjustLineHeightIfTooBig('id4');adjustFontSizeIfTooBig('id4');NotificationCenter.addObserver(null,relayoutMediaGrid_id5,'RangeChanged','id5')
adjustLineHeightIfTooBig('id6');adjustFontSizeIfTooBig('id6');adjustLineHeightIfTooBig('id7');adjustFontSizeIfTooBig('id7');fixupAllIEPNGBGs();fixAllIEPNGs('Media/transparent.gif');Widget.onload();applyEffects()
initializeMediaStream_id5()}
function onPageUnload()
{Widget.onunload();}
