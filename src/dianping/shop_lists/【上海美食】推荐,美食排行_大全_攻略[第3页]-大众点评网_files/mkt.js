!function(){function t(t,i){for(var n in i)t[n]=i[n];return t}var i="app-midas@0.6.12/js/cat.js",n="app-midas@0.6.12/js/cat.min.js",e="app-midas@0.6.12/js/mkt.js",_="app-midas@0.6.12/js/third-party.js",a="app-midas@0.6.12/js/third-party/haier.js",c="app-midas@0.6.12/js/third-party/pizzahut.js",m="app-midas@0.6.12/js/view/display-3-10.html.js",o="app-midas@0.6.12/js/view/display-3-12.html.js",s="app-midas@0.6.12/js/view/display-3-14.html.js",p="app-midas@0.6.12/js/view/display-3-15.html.js",r="app-midas@0.6.12/js/view/display-3-19.html.js",d="app-midas@0.6.12/js/view/display-4-10.html.js",h="app-midas@0.6.12/js/view/display-4-12.html.js",u="app-midas@0.6.12/js/view/display-4-14.html.js",l="app-midas@0.6.12/js/view/display-4-15.html.js",v="app-midas@0.6.12/js/view/display-4-19.html.js",F="app-midas@0.6.12/js/view/wrap-3.html.js",f="app-midas@0.6.12/js/view/wrap-4.html.js",I="jquery@~1.9.2",D="request@~0.2.4",g="json@~1.0.1",x="fx@^2.0.0",y="switch@~0.1.0",P=[i,n,e,_,a,c,m,o,s,p,r,d,h,u,l,v,F,f],j={},C=j;define(e,[I,D,g,x,y,_],function(t,i,n,e,_){function a(t){t.length&&document.hippo.mv("ad_b",t.join(","))}function c(t,i){var n=0,e=[];t.forEach(function(t,_){if(t.pos&&t.ads){var a=t.pos,c=t.ads;if(s(l+a).length){var m,o=s(l+a),p=s("<div></div>");c.forEach(function(t,a){if(t.html&&"string"==typeof t.html&&!/<link.*?>/i.test(t.html)&&!/<style.*?>/i.test(t.html)&&!/<script.*?>/i.test(t.html)){var c=t.html,o="J_DPMKT_Temp_"+_+"_"+a;m=s(c);try{u(m,i)}catch(r){}m.addClass(o).appendTo(p),t.effect&&"switch"===t.effect&&(m.addClass("J_DPMKT_switch J_mkt-slider-"+n),F.push(m),n++,t.effect_cfg&&v.push(t.effect_cfg))}try{t.hippo&&t.hippo.forEach(function(t){t&&e.push(t)})}catch(r){}}),""!=p.html()&&p.children().appendTo(o)}}}),a(e),m()}function m(){F.length&&F.forEach(function(t,i){var n=v[i];if(n.type&&-1!=n.type.indexOf("carousel")&&(new h).plugin("carousel",n.autoPlay?"autoPlay":"").init({CSPre:".J_mkt-slider-"+i,itemCS:"li",itemOnCls:"current",triggerCS:".DPMKTShower li",triggerOnCls:"current",containerCS:".DPMKTSlider",direction:n.direction||"top",duration:1e3*n.duration||1e3,interval:n.interval||3e3,triggerType:n.triggerType||"mouseenter"}),n.type&&-1!=n.type.indexOf("accordion")){var e=s(t).all("li"),_="current";e.on("mouseenter",function(t){e.removeClass(_),s(this).addClass(_)})}if(n.type&&-1!=n.type.indexOf("lantern")){var a,c,m=".J_mkt-slider-"+i,o=s(m),p=parseInt(o.css("width"));a=function(t){t&&t[0].css({cursor:"pointer",opacity:1})},c=function(t){t&&t[0].css({cursor:"default",opacity:.3})};var r,d=o.find(".DPMKT-block"),u=o.find(".slider-box"),e=o.find(".DPMKT-block li"),l="";l=d.hasClass("s-item")?"s-item":"DPMKT-list dl-txt";for(var F=3,f=e.length;f>F;F++)F%3==0&&(r=s("<ul></ul>").addClass("DPMKT-block "+l),u.append(r)),e.eq(F).appendTo(r);(new h).plugin("carousel","endless",n.autoPlay?"autoPlay":"").on("afterInit",function(){var t=o.find(".DPMKT-block"),i=o.find(".block-inner");i.css("height",t.eq(0).css("height")),t.each(function(t,i){s(i).css("left",p*t)}),o.find(".slide-count").html(t.length)}).on("switching",function(){o.find(".slide-index").html(this.expectIndex+1)}).on("navEnable",a).on("navDisable",c).init({CSPre:m,itemCS:".DPMKT-block",containerCS:".slider-box",prevCS:".prev",nextCS:".next",direction:"left",fx:{duration:1e3*n.duration||1e3},itemSpace:p})}})}function o(t){var i,n=r,e="post";t.request_type&&"jsonp"==t.request_type&&(n=d,e="get"),new n({url:t.server,data:t.query,method:e}).on("success",function(n){n&&(200===n.code||205===n.code)&&n.msg&&n.msg.msg&&n.msg.msg.groups&&(i=n.msg.msg.groups,c(i,t),205===n.code)}).send()}var s=t("jquery"),p=t("request"),r=(t("json"),p.Ajax),d=p.JSONP,h=(t("fx"),t("switch").Switch),u=t("./third-party"),l=".J_mkt-group-",v=[],F=[];i.init=function(t){o(t)}},{entries:P,map:t({"./third-party":_},C)}),define(_,[a,c],function(t,i,n,e,_){var a=t("./third-party/haier"),c=t("./third-party/pizzahut"),m=function(t){var i=new Image;i.src=t};n.exports=function(t,i){a(t,i,m),c(t,i,m)}},{entries:P,map:t({"./third-party/haier":a,"./third-party/pizzahut":c},C)}),define(a,[],function(t,i,n,e,_){n.exports=function(t,i,n){var e="http://event.dianping.com/midas/1activities/1859/index.html",_=i.query||{},a=function(i,_){~t.html().indexOf(e)&&(i.forEach(function(t){n(t)}),t.find("a").on("click",function(){!function(t){t.forEach(function(t){n(t)})}(_)}))},c=function(t){return t.match(/document.hippo.mv\(.*?\)/)[0].split(",")[1].replace(")","").split("_")[1].replace("'","")},m=t.html();switch(c(m)){case"1001":10===_.shopType&&a(["http://v.admaster.com.cn/i/a55664,b592518,c555,i0,m202,h,u","http://g.cn.miaozhen.com/x/k=2007227&p=6tTN7&dx=0&rt=2&ns=__IP__&ni=__IESID__&v=__LOC__&o="],["http://c.admaster.com.cn/c/a55664,b592518,c555,i0,m101,h,u","http://e.cn.miaozhen.com/r/k=2007227&p=6tTN7&dx=0&rt=2&ns=__IP__&ni=__IESID__&v=__LOC__&o=http%3A%2F%2Fevt.dianping.com%2Fmidas%2F1activities%2F1147%2Findex.html%3Ft%3D1"]),20===_.shopType&&a(["http://v.admaster.com.cn/i/a55664,b592520,c555,i0,m202,h,u","http://g.cn.miaozhen.com/x/k=2007227&p=6tTN9&dx=0&rt=2&ns=__IP__&ni=__IESID__&v=__LOC__&o="],["http://c.admaster.com.cn/c/a55664,b592520,c555,i0,m101,h,u","http://e.cn.miaozhen.com/r/k=2007227&p=6tTN9&dx=0&rt=2&ns=__IP__&ni=__IESID__&v=__LOC__&o=http%3A%2F%2Fevt.dianping.com%2Fmidas%2F1activities%2F1147%2Findex.html%3Ft%3D1"]),50===_.shopType&&a(["http://v.admaster.com.cn/i/a55664,b592520,c555,i0,m202,h,u","http://g.cn.miaozhen.com/x/k=2007227&p=6tTN9&dx=0&rt=2&ns=__IP__&ni=__IESID__&v=__LOC__&o="],["http://c.admaster.com.cn/c/a55664,b592520,c555,i0,m101,h,u","http://e.cn.miaozhen.com/r/k=2007227&p=6tTN9&dx=0&rt=2&ns=__IP__&ni=__IESID__&v=__LOC__&o=http%3A%2F%2Fevt.dianping.com%2Fmidas%2F1activities%2F1147%2Findex.html%3Ft%3D1"]),30===_.shopType&&a(["http://v.admaster.com.cn/i/a55664,b592521,c555,i0,m202,h,u","http://g.cn.miaozhen.com/x/k=2007227&p=6tTNA&dx=0&rt=2&ns=__IP__&ni=__IESID__&v=__LOC__&o="],["http://c.admaster.com.cn/c/a55664,b592521,c555,i0,m101,h,u","http://e.cn.miaozhen.com/r/k=2007227&p=6tTNA&dx=0&rt=2&ns=__IP__&ni=__IESID__&v=__LOC__&o=http%3A%2F%2Fevt.dianping.com%2Fmidas%2F1activities%2F1147%2Findex.html%3Ft%3D1"]);break;case"1003":case"1004":a(["http://v.admaster.com.cn/i/a55664,b592519,c555,i0,m202,h,u","http://g.cn.miaozhen.com/x/k=2009821&p=6veIa&dx=0&rt=2&ns=__IP__&ni=__IESID__&v=__LOC__&nd=__DRA__&np=__POS__&nn=__APP__&o="],["http://c.admaster.com.cn/c/a55664,b592519,c555,i0,m101,h,u","http://e.cn.miaozhen.com/r/k=2009821&p=6veIa&dx=0&ni=__IESID__&mo=__OS__&ns=__IP__&m0=__OPENUDID__&m0a=__DUID__&m1=__ANDROIDID1__&m1a=__ANDROIDID__&m2=__IMEI__&m4=__AAID__&m5=__IDFA__&m6=__MAC1__&m6a=__MAC__&ro=sm&nd=__DRA__&np=__POS__&nn=__APP__&vo=3b8e9d8e9&vr=2&o=http%3A%2F%2Fevent.dianping.com%2Fmidas%2F1activities%2F1859%2Findex.html"]),10===_.shopType&&a(["http://v.admaster.com.cn/i/a55664,b592519,c555,i0,m202,h,u","http://g.cn.miaozhen.com/x/k=2007227&p=6tTN8&dx=0&rt=2&ns=__IP__&ni=__IESID__&v=__LOC__&o="],["http://c.admaster.com.cn/c/a55664,b592519,c555,i0,m101,h,u","http://e.cn.miaozhen.com/r/k=2007227&p=6tTN8&dx=0&rt=2&ns=__IP__&ni=__IESID__&v=__LOC__&o=http%3A%2F%2Fevt.dianping.com%2Fmidas%2F1activities%2F1147%2Findex.html%3Ft%3D1"]),20===_.shopType&&a(["http://v.admaster.com.cn/i/a55664,b592521,c555,i0,m202,h,u","http://g.cn.miaozhen.com/x/k=2007227&p=6tTNA&dx=0&rt=2&ns=__IP__&ni=__IESID__&v=__LOC__&o="],["http://c.admaster.com.cn/c/a55664,b592521,c555,i0,m101,h,u","http://e.cn.miaozhen.com/r/k=2007227&p=6tTNA&dx=0&rt=2&ns=__IP__&ni=__IESID__&v=__LOC__&o=http%3A%2F%2Fevt.dianping.com%2Fmidas%2F1activities%2F1147%2Findex.html%3Ft%3D1"]),50===_.shopType&&a(["http://v.admaster.com.cn/i/a55664,b592521,c555,i0,m202,h,u","http://g.cn.miaozhen.com/x/k=2007227&p=6tTNA&dx=0&rt=2&ns=__IP__&ni=__IESID__&v=__LOC__&o="],["http://c.admaster.com.cn/c/a55664,b592521,c555,i0,m101,h,u","http://e.cn.miaozhen.com/r/k=2007227&p=6tTNA&dx=0&rt=2&ns=__IP__&ni=__IESID__&v=__LOC__&o=http%3A%2F%2Fevt.dianping.com%2Fmidas%2F1activities%2F1147%2Findex.html%3Ft%3D1"]),30===_.shopType&&a(["http://v.admaster.com.cn/i/a55664,b592520,c555,i0,m202,h,u","http://g.cn.miaozhen.com/x/k=2007227&p=6tTN9&dx=0&rt=2&ns=__IP__&ni=__IESID__&v=__LOC__&o="],["http://c.admaster.com.cn/c/a55664,b592520,c555,i0,m101,h,u","http://e.cn.miaozhen.com/r/k=2007227&p=6tTN9&dx=0&rt=2&ns=__IP__&ni=__IESID__&v=__LOC__&o=http%3A%2F%2Fevt.dianping.com%2Fmidas%2F1activities%2F1147%2Findex.html%3Ft%3D1"]);break;case"122":a(["http://v.admaster.com.cn/i/a55664,b592518,c555,i0,m202,h,u","http://g.cn.miaozhen.com/x/k=2007227&p=6tTN7&dx=0&rt=2&ns=__IP__&ni=__IESID__&v=__LOC__&o="],["http://c.admaster.com.cn/c/a55664,b592518,c555,i0,m101,h,u","http://e.cn.miaozhen.com/r/k=2007227&p=6tTN7&dx=0&rt=2&ns=__IP__&ni=__IESID__&v=__LOC__&o=http%3A%2F%2Fevt.dianping.com%2Fmidas%2F1activities%2F1147%2Findex.html%3Ft%3D1"])}return!0}},{entries:P,map:C}),define(c,[I],function(t,i,n,e,_){var a=t("jquery");n.exports=function(t,i,n){var e=function(t){return t.match(/document.hippo.mv\(.*?\)/)[0].split(",")[1].replace(")","").split("_")[1].replace("'","")},_=function(t,i){return t.replace(/\{(.+?)\}/g,function(t,n){return n in i?i[n]:t})},c=t.html(),m={},o="",s="http://g.cn.miaozhen.com/x/k=2006920&p={p}&dx=0&rt=2&ns=__IP__&ni=__IESID__&v=__LOC__&o=",p="http://e.cn.miaozhen.com/r/k=2006920&p={p}&ro=sm&ae=1001043&dx=0&rt=2&ns=__IP__&ni=__IESID__&v=__LOC__&vo=313add540&&vr=2&o={o}";switch(e(c)){case"1001":m.o="http%3A%2F%2Fevent.dianping.com%2Fmidas%2F1activities%2F1181%2Findex.html%3Futm_source%3Ddianping%26utm_medium%3DRightpicture%26utm_content%3DSearchresultspage%26utm_campaign%3D518%252D621Menurevamp",m.p="6tQUy",o=decodeURIComponent(m.o);break;case"1008":m.p="6tQUz",m.o="http%3A%2F%2Fevent.dianping.com%2Fmidas%2F1activities%2F1181%2Findex.html%3Futm_source%3Ddianping%26utm_medium%3DTopbanner%26utm_content%3DFinddiscountchannels%26utm_campaign%3D518%252D621Menurevamp",o=decodeURIComponent(m.o);break;case"1004":m.p="6tQV1",m.o="http%3A%2F%2Fevent.dianping.com%2Fmidas%2F1activities%2F1181%2Findex.html%3Futm_source%3Ddianping%26utm_medium%3DRightpicture%26utm_content%3DHomebusiness%26utm_campaign%3D518%252D621Menurevamp",o=decodeURIComponent(m.o);break;case"122":m.p="6tYdv",m.o="http%3A%2F%2Fevent.dianping.com%2Fmidas%2F1activities%2F1181%2Findex.html%3Futm_source%3Ddianping%26utm_medium%3DBanner%26utm_content%3Dsearchfoodpagebottombanner%26utm_campaign%3D518%252D621Menurevamp",o=decodeURIComponent(m.o)}return""===o?!1:void(~c.indexOf(o)&&(n(_(s,m)),t.find("a").each(function(t,i){var e=i.href;~e.indexOf(o)&&!function(t){a(i).on("click",function(){n(_(p,t))})}(m)})))}},{entries:P,map:C})}();
//# sourceMappingURL=js/mkt.js.map