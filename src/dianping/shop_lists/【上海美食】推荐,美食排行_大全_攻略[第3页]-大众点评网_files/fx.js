define("fx@2.0.0/lib/clock",[],function(a,b,c){var d={},e={};c.exports.addFx=function(a){var b=a.fps,c=d[b]||(d[b]=[]),f=e[b];c.push(a),f||(e[b]=setInterval(function(){for(var a,b=+new Date,d=c.length;d--;)(a=c[d])&&a.step(b)},Math.round(1e3/b)))},c.exports.removeFx=function(a){for(var b=a.fps,c=d[b]||(d[b]=[]),f=e[b],g=0,h=c.length;h>g;g++)c[g]===a&&c.splice(g,1);!c.length&&f&&(e[b]=clearInterval(f))},c.exports.isScheduled=function(a){var b=d[a.fps];if(b){if(b.indexOf)return-1!=b.indexOf(a);for(var c=0,e=b.length;e>c;++c)if(b[c]===a)return!0}return!1}}),define("fx@2.0.0/lib/frames",["util@~1.0.4","events@~1.0.5","./clock"],function(a,b,c){function d(a){f.call(this);var b=this.fps=a.fps||60;this.duration=a.duration||500,this.frameSkip=a.hasOwnProperty("frameSkip")?!!a.frameSkip:!0,this.frameInterval=1e3/b,this.frames=this.frames||Math.round(this.duration/this.frameInterval),this.transition=a.transition||function(a){return-(Math.cos(Math.PI*a)-1)/2}}var e=a("util"),f=a("events"),g=a("./clock");e.inherits(d,f),d.prototype.step=function(a){var b=this;if(b.frameSkip){var c=null!=b.time?a-b.time:0,d=c/this.frameInterval;b.time=a,b.frame+=d}else b.frame++;if(b.frame<b.frames){var e=b.transition(b.frame/b.frames);b.emit("progress",e)}else b.frame=b.frames,b.emit("progress",1),b.stop()},d.prototype.start=function(){var a=this;return a.time=null,a.frame=a.frameSkip?0:-1,a.emit("start"),g.addFx(a),a},d.prototype.stop=function(){var a=this;return a.isRunning()&&(a.time=null,g.removeFx(a),a.frame===a.frames?a.emit("complete"):a.emit("stop")),a},d.prototype.cancel=function(){var a=this;return a.isRunning()&&(a.time=null,g.removeFx(a),a.frame=a.frames,a.emit("cancel")),a},d.prototype.pause=function(){var a=this;return a.isRunning()&&(a.time=null,g.removeFx(a)),a},d.prototype.resume=function(){var a=this;return a.frame<a.frames&&!a.isRunning()&&g.addFx(a),a},d.prototype.isRunning=function(){return g.isScheduled(this)},c.exports=d}),define("fx@2.0.0/lib/fx",["util@~1.0.4","events@~1.0.5","./frames","./render","./parser"],function(a,b,c){function d(a,b){var c=this;f.call(this),b=b||{},this.renderOpts={unit:b.unit},this.framesOpts={duration:b.duration,fps:b.fps,frameSkip:b.frameSkip,frames:b.frames,transition:b.transition},this.element=a,this.link=b.link||"ignore";var d=this.start;this.start=i[this.link].call(this,function(){d.apply(c,arguments)})}var e=a("util"),f=a("events"),g=a("./frames"),h=a("./render"),i=(a("./parser"),{cancel:function(a){return function(){this.cancel(),a.apply(this,arguments)}},chain:function(a){function b(){var a=g.shift();e=!1,a?(e=!0,c(a)):f.emit("chainComplete")}function c(b){a.apply(b)}function d(a){e?g.push(a):(e=!0,c(a))}var e,f=this,g=f.__queue=f.__queue||[];return f.on("complete",b),function(){return d(arguments),f}},ignore:function(a){return function(){!this.isRunning()&&a.apply(this,arguments)}}});e.inherits(d,f),d.prototype.start=function(a,b,c){var d=this;if(arguments.length>1){var e=a;a={},a[e]=2==arguments.length?[b]:[b,c]}var f=new h(this.element,a,this.renderOpts),i=this.__frames=new g(this.framesOpts);i.on("progress",function(a){f.progress(a)});for(var j=["complete","start","stop","cancel"],k=0,l=j.length;l>k;++k)!function(a){i.on(a,function(){d.emit(a)})}(j[k]);i.start()},d.prototype.stop=function(){this.__frames&&(this.__frames.stop(),this.__frames.removeAllListeners(),this.__frames=null)},d.prototype.cancel=function(){this.__frames&&(this.__frames.cancel(),this.__frames.removeAllListeners(),this.__frames=null)},d.prototype.isRunning=function(){return this.__frames&&this.__frames.isRunning()},d.prototype.resume=function(){this.__frames&&this.__frames.resume()},d.prototype.pause=function(){this.__frames&&this.__frames.pause()},c.exports=d}),define("fx@2.0.0/lib/parser",["util@~1.0.4","hexrgb@~0.0.1"],function(a,b,c){function d(a,b,c){return(b-a)*c+a}var e=a("util"),f=a("hexrgb"),g={Color:{parse:function(a){return a.match(/^#[0-9a-f]{3,6}$/i)?f.hex2rgb(a,!0):(a=a.match(/(\d+),\s*(\d+),\s*(\d+)/))?[a[1],a[2],a[3]]:!1},compute:function(a,b,c){for(var e=[],f=0,g=a.length;g>f;++f)e.push(Math.round(d(a[f],b[f],c)));return e},serve:function(a){for(var b,c=[];b=a.shift();)c.push(Number(b));return c}},Number:{parse:parseFloat,compute:d,serve:function(a,b){return b?a+b:a}},String:{parse:function(){return!1},compute:function(a,b){return b},serve:function(a){return a}}};c.exports=function(a){var b;a=String(e.isFunction(a)?a():a);for(var c in g){var d=g[c],f=d.parse(a);if(f||0===f){b={value:f,parser:d};break}}return b=b||{value:a,parser:g.String}}}),define("fx@2.0.0/lib/render",["util@~1.0.4","./parser","jquery@~1.9.2"],function(a,b,c){function d(a,b,c){this.element=a=g(a),this.properties={},this.unit=c&&c.unit||!1;var d=this.froms={},h=this.tos={};for(var i in b){var j=b[i];if((e.isString(j)||e.isNumber(j))&&(j={to:j}),e.isArray(j)&&(j=null==j[1]?{to:j[0]}:{from:j[0],to:j[1]}),!j.hasOwnProperty("from")){var k=this.element.css(i);j.from="auto"===k?0:k}this.properties[i]=j}for(var i in this.properties)d[i]=f(this.properties[i].from),h[i]=f(this.properties[i].to)}var e=a("util"),f=a("./parser"),g=a("jquery"),h={};c.exports=d,d.prototype.compute=function(a,b,c){return{_:h,value:b.parser.compute(b.value,c.value,a),parser:b.parser}},d.prototype.progress=function(a){var b={};for(var c in this.froms){var d=this.compute(a,this.froms[c],this.tos[c]);b[c]=this.serve(d,this.properties[c].unit||this.unit)}this.element.css(b)},d.prototype.serve=function(a,b){return a._!==h&&(a=f(a)),a.parser.serve(a.value,b)}}),define("fx@2.0.0/lib/transitions",["util@~1.0.4"],function(a,b,c){function d(a,b){null==b?b=[]:e.isArray(b)||(b=[b]);var c=function(c){return a(c,b)};return c.easeIn=c,c.easeOut=function(c){return 1-a(1-c,b)},c.easeInOut=function(c){return(.5>=c?a(2*c,b):2-a(2*(1-c),b))/2},c}var e=a("util"),f={linear:function(a){return a}};f.extend=function(a){for(var b in a)f[b]=new d(a[b])},f.extend({Pow:function(a,b){return Math.pow(a,b&&b[0]||6)},Expo:function(a){return Math.pow(2,8*(a-1))},Circ:function(a){return 1-Math.sin(Math.acos(a))},Sine:function(a){return 1-Math.cos(a*Math.PI/2)},Back:function(a,b){return b=b&&b[0]||1.618,Math.pow(a,2)*((b+1)*a-b)},Bounce:function(a){for(var b,c=0,d=1;1;c+=d,d/=2)if(a>=(7-4*c)/11){b=d*d-Math.pow((11-6*c-11*a)/4,2);break}return b},Elastic:function(a,b){return Math.pow(2,10*--a)*Math.cos(20*a*Math.PI*(b&&b[0]||1)/3)}}),["Quad","Cubic","Quart","Quint"].forEach(function(a,b){f[a]=new d(function(a){return Math.pow(a,b+2)})}),c.exports=f}),define("fx@2.0.0/index",["./lib/fx","./lib/transitions"],function(a,b,c){var d=a("./lib/fx");c.exports=d,c.exports.Fx=d,c.exports.Transitions=a("./lib/transitions")},{main:!0});