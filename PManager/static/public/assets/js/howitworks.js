(function (lib, img, cjs, ss, an) {
var p; // shortcut to reference prototypes
lib.webFontTxtInst = {};
var loadedTypekitCount = 0;
var loadedGoogleCount = 0;
var gFontsUpdateCacheList = [];
var tFontsUpdateCacheList = [];
lib.ssMetadata = [];
lib.updateListCache = function (cacheList) {
	for(var i = 0; i < cacheList.length; i++) {
		if(cacheList[i].cacheCanvas)
			cacheList[i].updateCache();
	}
};
lib.addElementsToCache = function (textInst, cacheList) {
	var cur = textInst;
	while(cur != null && cur != exportRoot) {
		if(cacheList.indexOf(cur) != -1)
			break;
		cur = cur.parent;
	}
	if(cur != exportRoot) {
		var cur2 = textInst;
		var index = cacheList.indexOf(cur);
		while(cur2 != null && cur2 != cur) {
			cacheList.splice(index, 0, cur2);
			cur2 = cur2.parent;
			index++;
		}
	}
	else {
		cur = textInst;
		while(cur != null && cur != exportRoot) {
			cacheList.push(cur);
			cur = cur.parent;
		}
	}
};
lib.gfontAvailable = function(family, totalGoogleCount) {
	lib.properties.webfonts[family] = true;
	var txtInst = lib.webFontTxtInst && lib.webFontTxtInst[family] || [];
	for(var f = 0; f < txtInst.length; ++f)
		lib.addElementsToCache(txtInst[f], gFontsUpdateCacheList);
	loadedGoogleCount++;
	if(loadedGoogleCount == totalGoogleCount) {
		lib.updateListCache(gFontsUpdateCacheList);
	}
};
lib.tfontAvailable = function(family, totalTypekitCount) {
	lib.properties.webfonts[family] = true;
	var txtInst = lib.webFontTxtInst && lib.webFontTxtInst[family] || [];
	for(var f = 0; f < txtInst.length; ++f)
		lib.addElementsToCache(txtInst[f], tFontsUpdateCacheList);
	loadedTypekitCount++;
	if(loadedTypekitCount == totalTypekitCount) {
		lib.updateListCache(tFontsUpdateCacheList);
	}
};
// symbols:
(lib.Fill1 = function() {
	this.initialize(img.Fill1);
}).prototype = p = new cjs.Bitmap();
p.nominalBounds = new cjs.Rectangle(0,0,27,27);// helper functions:
function mc_symbol_clone() {
	var clone = this._cloneProps(new this.constructor(this.mode, this.startPosition, this.loop));
	clone.gotoAndStop(this.currentFrame);
	clone.paused = this.paused;
	clone.framerate = this.framerate;
	return clone;
}
function getMCSymbolPrototype(symbol, nominalBounds, frameBounds) {
	var prototype = cjs.extend(symbol, cjs.MovieClip);
	prototype.clone = mc_symbol_clone;
	prototype.nominalBounds = nominalBounds;
	prototype.frameBounds = frameBounds;
	return prototype;
	}
(lib.yrtyrtytry = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.lf(["#FD5C69","#F17F35"],[0,1],35.3,0,-35.2,0).s().p("AktAyQgVAAgPgPQgPgPAAgUQAAgUAPgOQAPgPAVAAIJbAAQAVAAAPAPQAPAOAAAUQAAAUgPAPQgPAPgVAAg");
	this.shape.setTransform(35.3,5);
	this.timeline.addTween(cjs.Tween.get(this.shape).wait(1));
}).prototype = getMCSymbolPrototype(lib.yrtyrtytry, new cjs.Rectangle(0,0,70.5,10), null);
(lib.tythhfh = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f().s("#FFFFFF").ss(3,0,0,4).p("AAjAeQAUAAAOAOQAOAOAAAUQAAATgOAOQgOANgUAAIh/AAQgMAAgJAJQgJAKAAAMQAAANAJAJQAJAJAMAAIA+AAIAAAsQAAANAJAKQAJAIAMAAQANAAAJgIQAJgKAAgNIAAgsIAFAAQAtAAAgggQAgggAAgsQAAgtggghQgggfgtAAIhGAAQgUAAgNgNQgPgOAAgUQAAgTAPgOQANgOAUAAIB8AAQANAAAJgJQAJgJAAgNQAAgMgJgJQgJgJgNAAIg7AAIAAgsQAAgNgJgJQgJgJgNAAQgMAAgJAJQgJAJAAANIAAAsIgFAAQgsAAghAgQgfAfAAAtQAAAtAfAgQAhAfAsAAg");
	this.shape.setTransform(14.5,26.2);
	this.shape_1 = new cjs.Shape();
	this.shape_1.graphics.lf(["#FC5E67","#F27D38"],[0,1],0,14.5,0,-14.4).s().p("AgVD8QgJgIAAgOIAAgsIg9AAQgNAAgKgJQgIgJgBgNQABgMAIgKQAKgIANgBIB+AAQAUAAAOgNQANgOAAgTQAAgVgNgNQgOgOgUAAIhGAAQgtAAgfgfQghggAAgsQAAguAhgfQAfggAtAAIAFAAIAAgsQAAgNAJgJQAJgIAMgBQANABAJAIQAIAJABANIAAAsIA7AAQANAAAJAJQAIAJABAMQgBANgIAJQgJAJgNAAIh9AAQgTAAgNAOQgOAOgBAUQABATAOAOQANAOATAAIBGAAQAtAAAhAeQAfAhAAAtQAAAsgfAgQghAggtAAIgEAAIAAAsQgBAOgIAIQgJAJgNAAQgLAAgKgJg");
	this.shape_1.setTransform(14.5,26.2);
	this.timeline.addTween(cjs.Tween.get({}).to({state:[{t:this.shape_1},{t:this.shape}]}).wait(1));
}).prototype = getMCSymbolPrototype(lib.tythhfh, new cjs.Rectangle(-1.5,-1.5,31.9,55.3), null);
(lib.tryrty = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f("#F87338").s().p("AipCqQhGhGAAhkQAAhiBGhHQBHhGBiAAQBjAABGBGQBHBHAABiQAABjhHBHQhGBGhjAAQhiAAhHhGg");
	this.shape.setTransform(24,24);
	this.timeline.addTween(cjs.Tween.get(this.shape).wait(1));
}).prototype = getMCSymbolPrototype(lib.tryrty, new cjs.Rectangle(0,0,48,48), null);
(lib.trhtrh = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f().s("#FFFFFF").ss(3,0,0,4).p("AjdAAQAAA6ApApQAqApA5AAQAxAAAmgfQAmgfALgvICJAAQANAAAIgJQAJgJAAgNQAAgMgJgJQgJgJgMAAIiJAAQgLgvgmgfQgmgfgxAAQg6AAgpApQgpApAAA5gAgCAAQAAAhgXAXQgYAXghAAQgfAAgYgXQgWgXAAghQAAgfAWgYQAYgXAfAAQAhAAAYAXQAXAYAAAfg");
	this.shape.setTransform(22.2,14);
	this.shape_1 = new cjs.Shape();
	this.shape_1.graphics.lf(["#42C1C2","#38C1CE"],[0,1],0,22.2,0,-22.2).s().p("Ai0BjQgpgpAAg6QAAg5ApgpQApgpA6AAQAyAAAlAfQAmAfALAvICJAAQAMAAAJAJQAJAJAAAMQAAANgJAJQgIAJgNAAIiJAAQgLAvgmAfQglAfgyAAQg5AAgqgpgAiJg3QgWAYAAAfQAAAhAWAXQAYAXAfAAQAhAAAYgXQAWgXAAghQAAgfgWgYQgYgXghAAQgfAAgYAXg");
	this.shape_1.setTransform(22.2,14);
	this.timeline.addTween(cjs.Tween.get({}).to({state:[{t:this.shape_1},{t:this.shape}]}).wait(1));
}).prototype = getMCSymbolPrototype(lib.trhtrh, new cjs.Rectangle(-1.5,-1.7,47.4,31.6), null);
(lib.trhrth = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f().s("#FFFFFF").ss(3,0,0,4).p("Ag2AfQALAvAmAfQAlAfAyAAQA6AAApgpQApgpAAg6QAAg5gpgpQgpgpg6AAQgyAAglAfQgmAfgLAvIiIAAQgNAAgJAJQgJAKAAALQAAANAJAJQAJAJANAAgAADAAQAAgfAXgYQAYgXAgAAQAhAAAXAXQAXAYAAAfQAAAhgXAXQgXAXghAAQggAAgYgXQgXgXAAghg");
	this.shape.setTransform(22.2,14);
	this.shape_1 = new cjs.Shape();
	this.shape_1.graphics.lf(["#44C0BE","#42C1C2"],[0,1],0,22.2,0,-22.2).s().p("AgFBtQgmgfgLgvIiIAAQgNAAgJgJQgJgJAAgNQAAgLAJgKQAJgJANAAICIAAQALgvAmgfQAlgfAyAAQA6AAApApQApApAAA5QAAA6gpApQgpApg6AAQgyAAglgfgAAag3QgXAYAAAfQAAAhAXAXQAYAXAgAAQAhAAAXgXQAXgXAAghQAAgfgXgYQgXgXghAAQggAAgYAXg");
	this.shape_1.setTransform(22.2,14);
	this.timeline.addTween(cjs.Tween.get({}).to({state:[{t:this.shape_1},{t:this.shape}]}).wait(1));
}).prototype = getMCSymbolPrototype(lib.trhrth, new cjs.Rectangle(-1.5,-1.8,47.5,31.7), null);
(lib.trhgfhhj = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f().s("#FFFFFF").ss(3,0,0,4).p("AANAOQgVAXghAAQghAAgXgXQgXgVAAgiQAAghAXgXQAXgWAhAAQAhAAAVAWQAXAXAAAhQACAggZAXgAgpi1Qg5AAgqApQgpAqAAA5QAAA4ApAqQApApA6AAQApAAAhgVIBgBgQAJAJANAAQANAAAJgJQAJgJAAgMQAAgNgJgJIhhhhQAWghAAgpQABg6gqgpQgqgpg4AAg");
	this.shape.setTransform(18.2,18.2);
	this.shape_1 = new cjs.Shape();
	this.shape_1.graphics.lf(["#42C1C2","#5FBB99"],[0,1],0,17.8,0,-17.7).s().p("ACCCtIhhhgQghAVgpAAQg6AAgpgpQgpgqAAg4QAAg5ApgqQAqgpA5AAQA4AAAqApQAqApgBA6QAAAogVAiIBgBhQAJAJAAAMQAAANgJAJQgJAJgNAAQgNAAgIgJgAhhhgQgWAVAAAiQAAAiAWAVQAYAXAggBQAhABAWgXQAXgWgBghQAAghgWgWQgWgYghABQgggBgYAYg");
	this.shape_1.setTransform(18.2,18.2);
	this.timeline.addTween(cjs.Tween.get({}).to({state:[{t:this.shape_1},{t:this.shape}]}).wait(1));
}).prototype = getMCSymbolPrototype(lib.trhgfhhj, new cjs.Rectangle(-1.5,-1.5,39.4,39.4), null);
(lib.thrhrhgh = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.lf(["#FD5C69","#F17F35"],[0,1],40,0,-40,0).s().p("AldAyQgVAAgPgPQgOgPAAgUQAAgUAOgPQAPgOAVAAIK7AAQAVAAAPAOQAOAPAAAUQAAAUgOAPQgPAPgVAAg");
	this.shape.setTransform(40,5);
	this.timeline.addTween(cjs.Tween.get(this.shape).wait(1));
}).prototype = getMCSymbolPrototype(lib.thrhrhgh, new cjs.Rectangle(0,0,80,10), null);
(lib.thgfh = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f().s("#FFFFFF").ss(3,0,0,4).p("ABPBSQAAAhgXAXQgXAXghAAQgfAAgYgXQgXgXAAghQAAggAXgYQAYgXAfAAQAhAAAXAXQAXAYAAAggAAAjdQgLAAgKAJQgJAJAAANIAACIQgvALgfAmQgfAlAAAyQAAA6ApApQApApA5AAQA6AAApgpQApgpAAg6QAAgygfglQgfgmgvgLIAAiIQAAgNgJgJQgJgJgNAAg");
	this.shape.setTransform(14,22.2);
	this.shape_1 = new cjs.Shape();
	this.shape_1.graphics.f("#38C1CE").s().p("AhiC1QgpgpAAg6QAAgyAfglQAfgmAvgLIAAiIQAAgNAJgJQAKgJALAAQANAAAJAJQAJAJAAANIAACIQAvALAfAmQAfAlAAAyQAAA6gpApQgpApg6AAQg5AAgpgpgAg3AaQgXAYAAAgQAAAhAXAXQAYAXAfAAQAhAAAXgXQAXgXAAghQAAgggXgYQgXgXghAAQgfAAgYAXg");
	this.shape_1.setTransform(14,22.2);
	this.timeline.addTween(cjs.Tween.get({}).to({state:[{t:this.shape_1},{t:this.shape}]}).wait(1));
}).prototype = getMCSymbolPrototype(lib.thgfh, new cjs.Rectangle(-1.7,-1.5,31.6,47.5), null);
(lib.tertre = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f().ls(["#FA635F","#F47741"],[0,1],0,23.4,0,-23.4).ss(3,0,0,4).p("AAAjvQBkAABGBGQBGBGAABjQAABjhGBGQhGBHhkAAQhiAAhGhHQhHhGAAhjQAAhjBHhGQBGhGBiAAg");
	this.shape.setTransform(24,24);
	this.shape_1 = new cjs.Shape();
	this.shape_1.graphics.f("#FFFFFF").s().p("AioCqQhHhGAAhkQAAhjBHhGQBGhGBiAAQBjAABGBGQBHBGAABjQAABkhHBGQhGBGhjAAQhiAAhGhGg");
	this.shape_1.setTransform(24,24);
	this.timeline.addTween(cjs.Tween.get({}).to({state:[{t:this.shape_1},{t:this.shape}]}).wait(1));
}).prototype = getMCSymbolPrototype(lib.tertre, new cjs.Rectangle(-1.5,-1.5,51,51), null);
(lib.tergrgrg = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f("#FC5E67").s().p("AA8g7IgLBsIhsALg");
	this.shape.setTransform(6,6);
	this.timeline.addTween(cjs.Tween.get(this.shape).wait(1));
}).prototype = getMCSymbolPrototype(lib.tergrgrg, new cjs.Rectangle(0,0,12,12), null);
(lib.tergg = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f().ls(["#FC5D67","#F27D38"],[0,1],0.4,0.4,-0.3,-0.3).ss(3,2,0,4).p("AlMlLIKZKX");
	this.shape.setTransform(33.3,33.2);
	this.timeline.addTween(cjs.Tween.get(this.shape).wait(1));
}).prototype = getMCSymbolPrototype(lib.tergg, new cjs.Rectangle(-2.1,-2.1,70.7,70.6), null);
(lib.teret = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f("#FC5E67").s().p("AhUgiICpAAIhVBFg");
	this.shape.setTransform(8.5,3.5);
	this.timeline.addTween(cjs.Tween.get(this.shape).wait(1));
}).prototype = getMCSymbolPrototype(lib.teret, new cjs.Rectangle(0,0,17,7), null);
(lib.terert = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f().ls(["#FC5D67","#F27D38"],[0,1],-50.9,39.9,50.7,-39.5).ss(3,2,0,4).p("AKi1AMgVDAqB");
	this.shape.setTransform(67.4,134.5);
	this.timeline.addTween(cjs.Tween.get(this.shape).wait(1));
}).prototype = getMCSymbolPrototype(lib.terert, new cjs.Rectangle(-2,-2,138.9,273.1), null);
(lib.teggfg = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f("#FC5E67").s().p("AgwAxIgLhsIB3B3g");
	this.shape.setTransform(6,6);
	this.timeline.addTween(cjs.Tween.get(this.shape).wait(1));
}).prototype = getMCSymbolPrototype(lib.teggfg, new cjs.Rectangle(0,0,12,12), null);
(lib.rwefe = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f().ls(["#FC5D67","#F27D38"],[0,1],-0.2,0.3,0.4,-0.4).ss(3,2,0,4).p("AFNlMIqZKZ");
	this.shape.setTransform(33.3,33.3);
	this.timeline.addTween(cjs.Tween.get(this.shape).wait(1));
}).prototype = getMCSymbolPrototype(lib.rwefe, new cjs.Rectangle(-2.1,-2.1,70.8,70.7), null);
(lib.rtret = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f().ls(["#FA635F","#F47741"],[0,1],-18.9,14.8,18.9,-14.7).ss(3,0,0,4).p("AC9iTQA9BPgMBhQgMBjhOA9QhPA9hhgMQhjgMg9hOQg9hPAMhhQAMhjBOg9QBPg9BhAMQBjAMA9BOg");
	this.shape.setTransform(24,24);
	this.shape_1 = new cjs.Shape();
	this.shape_1.graphics.f("#FFFFFF").s().p("AgcDuQhjgMg9hOQg9hPAMhhQAMhjBOg9QBPg9BhAMQBjAMA9BOQA9BPgMBhQgMBjhOA9QhCAzhQAAQgOAAgQgCg");
	this.shape_1.setTransform(24,24);
	this.timeline.addTween(cjs.Tween.get({}).to({state:[{t:this.shape_1},{t:this.shape}]}).wait(1));
}).prototype = getMCSymbolPrototype(lib.rtret, new cjs.Rectangle(-2,-1.7,51.6,51.3), null);
(lib.rtgrtf = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.lf(["#FD5C69","#F17F35"],[0,1],26.1,0,-25.9,0).s().p("AjRAyQgVAAgPgOQgOgPAAgVQAAgUAOgOQAPgPAVAAIGjAAQAVAAAPAPQAOAOAAAUQAAAVgOAPQgPAOgVAAg");
	this.shape.setTransform(26,5);
	this.timeline.addTween(cjs.Tween.get(this.shape).wait(1));
}).prototype = getMCSymbolPrototype(lib.rtgrtf, new cjs.Rectangle(0,0,52,10), null);
(lib.rhh = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f().s("#FFFFFF").ss(3,0,0,4).p("AhhgpQAAApAWAhIhhBhQgJAJAAAMQAAANAJAJQAJAJANAAQANAAAIgJIBihhQAhAWAoAAQA6AAApgpQApgpAAg5QAAg6gpgpQgpgpg6AAQg5AAgpApQgpApAAA6gAgMhhQAWgWAgAAQAhAAAXAWQAXAYAAAgQAAAhgXAWQgXAXghAAQggAAgWgXQgXgWAAghQgBghAYgXg");
	this.shape.setTransform(18.2,18.2);
	this.shape_1 = new cjs.Shape();
	this.shape_1.graphics.lf(["#42C1C2","#5FBB98"],[0,1],0,18.2,0,-18.2).s().p("AisCtQgJgJAAgNQAAgMAJgKIBhhgQgWghAAgpQAAg6ApgpQApgpA5AAQA6AAApApQApApAAA6QAAA5gpApQgpApg6AAQgoAAghgWIhiBhQgIAJgNAAQgNAAgJgJgAgMhgQgYAWABAhQAAAhAXAWQAWAXAgAAQAhAAAXgXQAXgWAAghQAAgggXgXQgXgYghAAQggAAgWAYg");
	this.shape_1.setTransform(18.2,18.2);
	this.timeline.addTween(cjs.Tween.get({}).to({state:[{t:this.shape_1},{t:this.shape}]}).wait(1));
}).prototype = getMCSymbolPrototype(lib.rhh, new cjs.Rectangle(-1.5,-1.5,39.5,39.4), null);
(lib.rgrgfg = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f("#FFFFFF").s().p("AipCqQhGhGAAhkQAAhiBGhHQBHhGBiAAQBjAABGBGQBHBHAABiQAABjhHBHQhGBGhjAAQhiAAhHhGg");
	this.shape.setTransform(24,24);
	this.timeline.addTween(cjs.Tween.get(this.shape).wait(1));
}).prototype = getMCSymbolPrototype(lib.rgrgfg, new cjs.Rectangle(0,0,48,48), null);
(lib.rgfdhh = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.lf(["#3CC1C8","#5EBB9C"],[0,1],0,44.4,0,-44.4).s().p("AlxJnQgnAAgUgYQgTgXAFglIA1kJQAHglAZgYQARgSAZgKQAEgCCaguIAvgeIAAggQg7gggjg6Qghg5AAhCQgegFgUgVQgTgVAAgbQAAgXAOgRIgBg9QAAhDAeg9QADgGAHgDQAHgCAHADQAHAEACAGQADAIgEAHQgVArgDAvQgCAZABAdQAJgEAKgCIAAgYQAAgSAJgPQAJgPAQgJQBKglBUgJQCBgNB5A/QAcAOAFAeQADAPgBASQAKADAJADIAAghQAAhqhMhMQhLhLhrAAQg1AAgwAVQgwAUglAmQgFAGgIAAQgHAAgGgFQgFgFAAgIQAAgHAFgFQAqgtA3gXQA3gXA8AAQB5AABXBWQBWBWAAB5IAAA9QAOARAAAXQAAAbgUAVQgTAVgeAFIAAADQAABEgkA6QgiA3g7AfIAAAdIAwAgICdAvQA9AZANBAIA1EJQAFAlgTAXQgUAYgngBIjSAAQgIAAgFgEQgFgGAAgIQAAgGAFgGQAFgFAIgBIBSAAIAAipQAAgjAGgmQAMhNAhg0IhegbIgBAAQgiBXg1AwQgzAsg5AAQg4gBgzgtQg1gwgihXIhlAdQAhA0AMBNQAGAmAAAjIAACpIE9AAQAHABAGAFQAFAGAAAGQAAAIgFAGQgGAFgHAAgAFsJDQAcAAAJgLQAJgKgDgWIg0kHQgHgfgXgSQgeAugLBJQgGAmABAbIAACqIAgAAIA1ABgAliERIg0EHQgDAWAJAKQAJALAcAAIBVgBIAAipQAAgxgLguQgMg3gXgjQgXASgHAfgAgSFAQASAEATgDIgCgUIggAAgABMD6IgDACIgDACIgDABIgDAAIgNAeIADAZQBDgiArhrIgIgCgAicCnQAoBmBAAlIADgUIgOgfQgHAAgKgLIgyg0IgZgagAgfDtIAMAcIAnAAIAMgcIgggXgAAdC+IAgAYIA+hAIgcgUgAh5CWIA+BAIAggYIhCg8gAhKBjIBKBDIBLhCIAAgRQhLAZhKgZgAgDmCQhgAAhXAsQgPAGAAASIAACsQAAAqARAoQAQAnAfAcQAvAsA9AKQA4AIA2gXQA3gXAhgvQAjgzAAhAIAAisQAAgQgPgJQhbgvhjAAIgCABgADwi3QAggKAAgbQAAgbgggKgAkOjcQAAAbAhAKIAAhKQghAKAAAbg");
	this.shape.setTransform(44.4,61.5);
	this.timeline.addTween(cjs.Tween.get(this.shape).wait(1));
}).prototype = getMCSymbolPrototype(lib.rgfdhh, new cjs.Rectangle(0,0,88.8,123), null);
(lib.rgdgd = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f("#000000").s().p("AgmBSIgIgJQgBAAAAAAQAAgBAAAAQgBgBAAAAQAAgBAAAAQAAgBAAAAQAAgBABAAQAAgBAAAAQAAgBABAAIBBhCIhBhAQgBgBAAAAQAAgBAAAAQgBgBAAAAQAAgBAAgBIACgDIAIgJQABAAAAAAQABgBAAAAQABAAAAAAQABAAAAAAIAEABIBNBOIACADQAAABAAAAQAAABgBAAQAAABAAAAQAAABgBAAIhNBOIgEABQAAAAgBAAQAAAAgBAAQgBAAAAAAQAAgBgBAAg");
	this.shape.setTransform(25.9,11.5);
	this.shape_1 = new cjs.Shape();
	this.shape_1.graphics.f("#000000").s().p("AAfBSIhNhOQgBAAAAgBQAAAAAAgBQgBAAAAgBQAAAAAAgBIACgDIBNhOIAEgBQAAAAABAAQAAAAABAAQAAAAABABQAAAAABAAIAIAJIACADQAAABAAABQAAAAgBABQAAAAAAABQAAAAgBABIhBBAIBBBCQABAAAAABQAAAAAAABQABAAAAABQAAAAAAABQAAAAAAABQAAAAgBABQAAAAAAABQAAAAgBAAIgIAJQgBAAAAABQAAAAgBAAQAAAAgBAAQgBAAAAAAQgBAAAAAAQgBAAAAAAQgBAAAAAAQAAgBgBAAg");
	this.shape_1.setTransform(4.9,11.5);
	this.shape_2 = new cjs.Shape();
	this.shape_2.graphics.f("#000000").s().p("AgbByIgKgDQgBAAAAAAQgBAAAAAAQAAgBgBAAQAAAAAAgBQgBAAAAgBQAAAAAAgBQAAAAAAgBQAAAAAAgBIA+jXQAAAAABgBQAAAAAAAAQAAgBABAAQAAgBABAAIAEgBIAKADIADADIABAEIg+DXQAAAAAAABQAAAAgBABQAAAAgBAAQAAABgBAAIgCABIgCgBg");
	this.shape_2.setTransform(15.4,11.5);
	this.timeline.addTween(cjs.Tween.get({}).to({state:[{t:this.shape_2},{t:this.shape_1},{t:this.shape}]}).wait(1));
}).prototype = getMCSymbolPrototype(lib.rgdgd, new cjs.Rectangle(0,0,30.8,23), null);
(lib.refgfdgfd = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.lf(["#3BC1C8","#5EBB9B"],[0,1],0,43.3,0,-43.2).s().p("AlxJnQgoAAgTgYQgTgXAFglIAAgBIA1kIQAKgyAqgbIApgSIC6guIAAgdQgdgPgYgXQgygwgRhDIgIg8QgsgIgSglQgSglAaghIAAiBQAAgcALghQACgHAHgDQAHgDAHACQAHADADAGQADAHgCAHQgJAZAAAcQgBAUABBOQAFgDANgDIAAgYQAAgSAKgPQAJgQAQgIQBKglBUgIQCBgNB5A+QAbAOAGAeQADAQgCARQAIABAKAEIAAhlQAAghgQgiQgfhDhNgTQhRgVgrgnQgEgEgFAAQgEAAgEAEQgrAnhRAVQguAKgdAdQgGAGgHgBQgIAAgFgFQgFgFAAgIQAAgHAGgGQAkgjA3gNQBIgSAlgiQAOgNASAAQATAAAOANQAlAiBIASQBeAXAnBVQASAqAAAmIAACAQAaAhgRAmQgRAlguAIIAAADQAABEgjA5QgjA4g6AeIAAAcIDJAyQBBAZANBCIAQBOQABAIgEAGQgEAGgIACQgHABgGgEQgGgEgCgHIgPhPQgHgjgegTIgfgNIizgtQgLAogfAWQgdAVglAAQgkAAgdgVQgfgWgLgoIi0AtIgeANQgeATgHAjIg0EHQgDAWAJALQAJAKAWAAIBbAAIAAiqQAAgHAGgFQAFgGAHAAQAIAAAFAGQAFAFAAAHIAACqIHlAAIAAiqQAAgHAGgFQAFgGAHAAQAIAAAFAGQAFAFAAAHIAACqQAngBAuABQAcAAAJgKQAIgJgCgYIgUhlQgCgHAFgGQAEgHAHgBQAHgBAHAEQAGAEABAHIAVBmQADAQgEAQQgDASgLAMQgTAXgnAAgAhKCKQACAeAWAUQAVAUAdAAQAeAAAVgUQAWgVACgdIAAgaQhLAZhKgZgAi7k5QgPAHAAARIAACsQAABvBcA9QBeA+BlgwQA5gaAfgyQAegxAAg6IAAisQAAgRgPgHQhbgwhiAAQhhAAhZAtgADviaQAhgKAAgbQAAgbghgKgAkOi/QAAAcAgAJIAAhKQggAKAAAbg");
	this.shape.setTransform(44.4,61.5);
	this.shape_1 = new cjs.Shape();
	this.shape_1.graphics.f("#3BC1C8").s().p("AAABLQgdAAgWgTQgVgSAAgbIAAgvQAAgQALgLQAMgLAPAAIBFAAQAQAAALALQALAMAAAPIAAAvQAAAbgVASQgWATgdAAgAgkgeIAAApQAAALALAJQALAIAOAAIABAAQAOAAALgIQALgJAAgLIAAgvQAAgBAAAAQgBAAAAgBQAAAAAAAAQgBAAAAAAIhFAAQgCAAAAAIg");
	this.shape_1.setTransform(57.6,108.1);
	this.timeline.addTween(cjs.Tween.get({}).to({state:[{t:this.shape_1},{t:this.shape}]}).wait(1));
}).prototype = getMCSymbolPrototype(lib.refgfdgfd, new cjs.Rectangle(0,0,88.8,123), null);
(lib.hhfhfh = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f().s("#FFFFFF").ss(3,0,0,4).p("AisisQgJAJAAANQAAAMAJAJIBhBhQgWAhAAApQAAA6ApApQApApA5AAQA6AAApgpQApgpAAg6QAAg5gpgpQgpgpg6AAQgoAAgiAVIhghhQgJgIgNAAQgNAAgJAJgAgMgNQAVgXAhAAQAgAAAYAXQAXAXAAAgQAAAhgXAXQgYAXggAAQgfAAgXgXQgXgXAAggQgBghAYgXg");
	this.shape.setTransform(18.2,18.2);
	this.shape_1 = new cjs.Shape();
	this.shape_1.graphics.f("#38C1CE").s().p("Ag4CNQgpgpAAg6QAAgpAWghIhhhhQgJgIAAgNQAAgNAJgJQAJgJANAAQANAAAIAIIBhBhQAigVAoAAQA6AAApApQApApAAA5QAAA6gpApQgpApg6AAQg5AAgpgpgAgNgNQgXAXABAgQgBAhAXAXQAXAXAgAAQAgAAAXgXQAYgXAAghQAAghgYgWQgWgWghAAQghAAgWAWg");
	this.shape_1.setTransform(18.2,18.2);
	this.timeline.addTween(cjs.Tween.get({}).to({state:[{t:this.shape_1},{t:this.shape}]}).wait(1));
}).prototype = getMCSymbolPrototype(lib.hhfhfh, new cjs.Rectangle(-1.5,-1.5,39.4,39.4), null);
(lib.hgfhhj = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f().s("#FFFFFF").ss(3,0,0,4).p("AAADeQANAAAJgJQAJgJAAgNIAAiIQAvgLAfgmQAfgmAAgxQAAg6gpgpQgpgpg6AAQg5AAgpApQgpApAAA6QAAAxAfAmQAfAmAvALIAACIQAAANAJAJQAJAJAMAAgAhOhSQAAggAXgXQAYgXAfAAQAhAAAXAXQAXAXAAAgQAAAhgXAXQgXAXghAAQgfAAgYgXQgXgXAAghg");
	this.shape.setTransform(14,22.2);
	this.shape_1 = new cjs.Shape();
	this.shape_1.graphics.lf(["#42C1C2","#5EBB98"],[0,1],0,13.7,0,-13.6).s().p("AgVDVQgJgJAAgNIAAiIQgvgLgfgmQgfglAAgyQAAg6ApgpQApgpA5AAQA6AAApApQApApAAA6QAAAygfAlQgfAmgvALIAACIQAAANgJAJQgJAJgNAAQgMAAgJgJgAg3iJQgXAXAAAgQAAAhAXAYQAYAWAfAAQAhAAAXgWQAXgYAAghQAAgggXgXQgXgXghAAQgfAAgYAXg");
	this.shape_1.setTransform(14,22.2);
	this.timeline.addTween(cjs.Tween.get({}).to({state:[{t:this.shape_1},{t:this.shape}]}).wait(1));
}).prototype = getMCSymbolPrototype(lib.hgfhhj, new cjs.Rectangle(-1.7,-1.5,31.6,47.4), null);
(lib.gre45 = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f("#49BFB8").s().p("AhGAnIAAgpIAZAAQAyAAAkgkIAeAeQgvAvhFAAg");
	this.shape.setTransform(47.2,53.1);
	this.shape_1 = new cjs.Shape();
	this.shape_1.graphics.f("#45C0BD").s().p("AgUBXQgLAAgGgIQgGgIACgLIAqiSIAqALIgjB4IAjAAIAAAqg");
	this.shape_1.setTransform(42.2,39.9);
	this.shape_2 = new cjs.Shape();
	this.shape_2.graphics.f("#5DBB9B").s().p("AgUCUIAAknIApAAIAAEng");
	this.shape_2.setTransform(71.8,112);
	this.shape_3 = new cjs.Shape();
	this.shape_3.graphics.f("#5DBB9B").s().p("AgUCUIAAknIApAAIAAEng");
	this.shape_3.setTransform(16.9,112);
	this.shape_4 = new cjs.Shape();
	this.shape_4.graphics.f("#45C0BD").s().p("AgdAeQgMgMAAgSQAAgQAMgNQANgMAQAAQASAAAMAMQAMANAAAQQAAASgMAMQgMAMgSAAQgQAAgNgMg");
	this.shape_4.setTransform(57,35.9);
	this.shape_5 = new cjs.Shape();
	this.shape_5.graphics.f("#45C0BD").s().p("AgdAeQgMgMAAgSQAAgQAMgNQAMgMARAAQARAAANAMQAMANAAAQQAAASgMAMQgNAMgRAAQgQAAgNgMg");
	this.shape_5.setTransform(31.7,35.9);
	this.shape_6 = new cjs.Shape();
	this.shape_6.graphics.f().s("#FFFFFF").ss(1,0,0,4).p("AD9B/Ih+AAIAAhiQA6ghAig6QAig7AAhEQAjAAAZgZQAZgZAAgjQAAgjgZgZQgZgYgjAAIAAgrQAAhghEhEQhDhEhhAAIj9AAQgIAAgHAGQgGAGAAAJQAAA6AkAtQgkA7AABGIAAAWQgjAAgYAYQgZAZAAAjQAAAjAZAZQAYAZAjAAQAABEAiA7QAiA6A7AhIAABiIh/AAQhOAAg4A4Qg4A3AABPIAAE9IAqAAIAAk9QAAg+AsgqQArgsA9AAICxAAIAiBDIgqE3QgBAKAHAHIBAA/QAGAHAIAAQAIAAAGgHIABAAIA/g/QAHgHgBgKIgqk3IAihDICxAAQA9AAAsAsQArAqAAA+IAAE9IAqAAIAAk9QAAhPg3g3Qg4g4hPAAgAjTi9IAAiIQAigUAWggQAWghAFgnQAUAHAYAAIDWAAQAHAkAVAfQAVAfAgATIAACIQAABXg+A+Qg9A9hYAAQhXAAg+g9Qg+g+AAhXgAjTl8QABg0AYgtQAJAGAJAFQgDA2goAjgAAVpPQBPAAA3A4QA4A4AABOIAAAYQgmgjgEg2QgBgIgFgGQgHgFgIAAIjoAAQguAAgkgeQgjgegIgugAj9joQgRAAgNgMQgMgMAAgSQAAgRAMgNQANgMARAAgAD9k8QASAAAMAMQANANAAARQAAASgNAMQgMAMgSAAgABUB/IioAAIAAhPQBUAeBUgegAgcCpIA5AAIgVAqIgPAAgAAAJGIgogqIAmkfIAFAAIAmEhg");
	this.shape_6.setTransform(44.4,63.4);
	this.shape_7 = new cjs.Shape();
	this.shape_7.graphics.lf(["#5FBB99","#39C2CD"],[0,1],0,63.2,0,-63.1).s().p("AgOJzIhAg/QgHgIACgKIApk2IghhDIiyAAQg9AAgrArQgrAsAAA9IAAE8IgqAAIAAk8QgBhPA4g4QA4g3BOAAIB/AAIAAhiQg7ghghg6Qgjg7AAhEQgjAAgYgZQgZgYAAgkQAAgjAZgYQAYgZAjAAIAAgWQABhGAjg7QgjgtgBg5QAAgKAHgGQAGgGAIAAID9AAQBhAABEBFQBDBEAABfIAAArQAkAAAYAZQAZAYAAAjQAAAkgZAYQgYAZgkAAQAABEghA7QgjA6g6AhIAABiIB+AAQBPAAA4A3QA3A4AABPIAAE8IgpAAIAAk8QAAg9gsgsQgrgrg+AAIiwAAIgjBDIAqE2QACALgIAHIg/A/IAAAAQgHAHgIAAQgIAAgGgHgAgoIdIAoApIApgoIgnkgIgDAAgAgHDTIAPAAIAVgqIg5AAgAhTB/ICoAAIAAhPQhVAehTgegAibl5QgVAggiAUIAACIQAABYA+A9QA9A9BXAAQBXAAA/g9QA9g9ABhYIAAiIQghgTgVgfQgVgfgHglIjVAAQgZABgTgHQgGAngWAhgAD9jnQASAAANgNQAMgMAAgSQAAgRgMgMQgNgNgSAAgAkakvQgNAMAAARQAAASANAMQAMANARAAIAAhVQgRAAgMANgAiloDQAjAeAvAAIDnAAQAIAAAGAFQAHAGAAAJQAEA1AnAjIAAgYQAAhOg5g4Qg3g3hPgBIjlAAQAHAuAkAegAjSl8IAAADQAngjADg2QgJgFgJgGQgXAugBAzg");
	this.shape_7.setTransform(44.4,63.4);
	this.timeline.addTween(cjs.Tween.get({}).to({state:[{t:this.shape_7},{t:this.shape_6},{t:this.shape_5},{t:this.shape_4},{t:this.shape_3},{t:this.shape_2},{t:this.shape_1},{t:this.shape}]}).wait(1));
}).prototype = getMCSymbolPrototype(lib.gre45, new cjs.Rectangle(-1,-1,90.7,128.8), null);
(lib.ggrrth = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f("#FC5E67").s().p("AhUgiICpAAIhVBFg");
	this.shape.setTransform(8.5,3.5);
	this.timeline.addTween(cjs.Tween.get(this.shape).wait(1));
}).prototype = getMCSymbolPrototype(lib.ggrrth, new cjs.Rectangle(0,0,17,7), null);
(lib.Sponsor = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f("#222222").s().p("AgfAxIAAhfIAZAAIAAAPQAFgIAJgFQAKgFANABIAAAbQgHgBgHABQgHACgGADQgEAEgDAGIAAA3g");
	this.shape.setTransform(74,12.1);
	this.shape_1 = new cjs.Shape();
	this.shape_1.graphics.f("#222222").s().p("AgZAtQgMgFgIgMQgHgLAAgRQAAgQAHgLQAIgLAMgGQAMgGANAAQAOAAAMAGQAMAGAHALQAIALAAAQQAAARgIALQgHAMgMAFQgMAGgOAAQgNAAgMgGgAgSgSQgFAIAAAKQAAALAFAHQAHAIALAAQAMAAAGgIQAHgHAAgLQAAgKgHgIQgGgHgMAAQgLAAgHAHg");
	this.shape_1.setTransform(63.7,12.2);
	this.shape_2 = new cjs.Shape();
	this.shape_2.graphics.f("#222222").s().p("AgWAwQgKgCgHgEIAAgXQAIAFAKACQAJADAJAAQAHAAAEgCQAFgBAAgEQAAgEgGgDQgFgDgHgCIgQgFQgIgEgFgFQgGgGAAgKQAAgMAGgFQAFgIAJgCQAKgDAKAAQAJABAJACIAQAFIAAAXIgKgFIgLgDIgMgBIgGAAIgFACQAAABgBAAQAAABAAAAQAAABgBABQAAAAAAABQAAAEAGADIAMAFIAQAGQAIACAGAGQAFAGAAAKQAAALgGAHQgGAGgKADQgJADgLAAQgLAAgKgDg");
	this.shape_2.setTransform(53.1,12.2);
	this.shape_3 = new cjs.Shape();
	this.shape_3.graphics.f("#222222").s().p("AAUAyIAAg3QAAgKgFgFQgGgEgIAAQgGAAgGADQgFAEgDAFIAAA+IgcAAIAAhgIAZAAIAAANQAFgHAIgEQAIgEAKAAQAMAAAJAFQAJAFAEAJQAFAJAAALIAAA7g");
	this.shape_3.setTransform(42.4,12.1);
	this.shape_4 = new cjs.Shape();
	this.shape_4.graphics.f("#222222").s().p("AgZAtQgMgFgIgMQgHgLAAgRQAAgQAHgLQAIgLAMgGQAMgGANAAQAOAAAMAGQAMAGAHALQAIALAAAQQAAARgIALQgHAMgMAFQgMAGgOAAQgNAAgMgGgAgSgSQgFAIAAAKQAAALAFAHQAHAIALAAQAMAAAGgIQAHgHgBgLQABgKgHgIQgGgHgMAAQgLAAgHAHg");
	this.shape_4.setTransform(30.5,12.2);
	this.shape_5 = new cjs.Shape();
	this.shape_5.graphics.f("#222222").s().p("Ag0BIIAAiMIAYAAIAAAPQAFgHAIgFQAJgFAMAAQAPAAALAHQAKAHAFAMQAGALAAAOQAAANgGAKQgFAMgKAHQgLAHgPAAQgKAAgIgDQgIgFgFgEIAAA2gAgQgqQgFAEgEAHIAAAXQAEAGAFAEQAHAEAJABQAIAAAFgEQAGgDADgGQADgGAAgHQAAgIgDgGQgDgGgGgEQgFgEgIAAQgJAAgHAFg");
	this.shape_5.setTransform(18.6,14.3);
	this.shape_6 = new cjs.Shape();
	this.shape_6.graphics.f("#222222").s().p("AgcBFQgNgDgLgGIAAgdQAMAJANADQANADAMABQALAAAHgEQAHgDAAgHQAAgHgGgEQgGgDgIgEIgSgGQgJgDgJgFQgIgFgGgIQgFgHgBgNQAAgOAIgJQAGgIAMgFQAMgEAOAAQALAAAMADQAMADAJAFIAAAcQgJgGgLgDQgLgDgMgBQgLAAgGAEQgFADAAAHQAAAFAFAFQAGADAJADIARAGQAKAEAJAFQAIAEAGAIQAFAIABAMQgBAQgHAJQgIAKgMADQgMAEgOAAQgPAAgNgEg");
	this.shape_6.setTransform(6.3,10);
	this.timeline.addTween(cjs.Tween.get({}).to({state:[{t:this.shape_6},{t:this.shape_5},{t:this.shape_4},{t:this.shape_3},{t:this.shape_2},{t:this.shape_1},{t:this.shape}]}).wait(1));
}).prototype = getMCSymbolPrototype(lib.Sponsor, new cjs.Rectangle(-2,0,81.7,24), null);
(lib.OGiExchange = function(mode,startPosition,loop) {
if (loop == null) { loop = false; }	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f("#000000").s().p("AgUAtQgNgFgHgMQgIgLAAgRQAAgMAFgKQAEgKAIgGQAHgGAJgDQAIgDAIAAQAOAAAKAFQAKAGAGAIQAGAJABAKQABALgCAKIhDAAQACAHAFAFQAFAEAHACQAGACAIAAQAIAAAIgBIANgFIAAAWIgQAFIgTABQgPAAgMgGgAgIgaQgGACgDAFQgDAFAAAGIAqAAQAAgEgBgEQgCgFgEgDQgFgFgIAAQgFABgFACg");
	this.shape.setTransform(130.9,12.2);
	this.shape_1 = new cjs.Shape();
	this.shape_1.graphics.f("#000000").s().p("AgXBHQgKgDgIgEIAAgZQAHAFAKADQAJACAKAAQAIAAAHgCQAHgCAEgGQAFgFgBgJIAAgJQgEAFgIAEQgIADgKABQgQAAgKgIQgKgGgGgMQgFgKAAgOQAAgNAFgMQAGgMAKgGQAKgIAQAAQAMAAAIAFQAJAGAFAGIAAgOIAYAAIAABdQAAARgIAMQgHALgNAEQgNAFgNAAQgLAAgLgCgAgMgsQgGADgDAGQgCAGAAAIQAAAIACAGQADAGAGACQAFAEAIABQAIgBAHgFQAGgDADgGIAAgYQgDgGgGgFQgHgEgIgBQgIABgFAEg");
	this.shape_1.setTransform(118.9,14.4);
	this.shape_2 = new cjs.Shape();
	this.shape_2.graphics.f("#000000").s().p("AAUAxIAAg3QAAgJgFgEQgGgGgIAAQgGABgGADQgFAFgDAEIAAA9IgcAAIAAheIAZAAIAAAMQAFgHAIgEQAIgEAKgBQAMABAJAFQAJAFAEAJQAFAJAAALIAAA6g");
	this.shape_2.setTransform(107.2,12);
	this.shape_3 = new cjs.Shape();
	this.shape_3.graphics.f("#000000").s().p("AgjAwQgHgEgFgGQgEgHAAgJQAAgKADgGQAEgGAGgDQAHgEAHgBQAHgCAIAAIAKABIAMACIAAgEQAAgGgGgFQgGgFgKAAQgKABgJACIgPAEIAAgXIAQgFQAKgCALAAQAOAAAKAEQALAFAGAKQAFAJAAAQIAAAdQAAAEACACIAFABIADAAIACgBIAAASIgHACIgIABQgHAAgGgDQgFgCgDgGQgHAGgJADQgHADgLAAQgJAAgIgDgAgNAHQgEACgDADQgDADAAAEQAAAGAEADQAFADAGAAQAGAAAEgCQAGgCAFgEIAAgPIgIgCIgIAAQgFAAgFABg");
	this.shape_3.setTransform(95.8,12.2);
	this.shape_4 = new cjs.Shape();
	this.shape_4.graphics.f("#000000").s().p("AAUBGIAAg4QAAgKgFgEQgGgEgIAAQgGAAgGAEQgFADgDAFIAAA+IgcAAIAAiLIAcAAIAAA1QAFgGAHgDQAHgDAJAAQAMAAAJAFQAJAGAEAJQAFAIAAAKIAAA8g");
	this.shape_4.setTransform(84.3,10);
	this.shape_5 = new cjs.Shape();
	this.shape_5.graphics.f("#000000").s().p("AgOAuQgMgGgIgKQgHgMAAgQQAAgNAEgLQAFgJAIgHQAIgGAJgDQAJgDAKAAQAIAAAHABQAIADAGADIAAAYQgFgDgGgCQgHgCgHAAQgIAAgHADQgFADgFAGQgEAFAAAJQAAAJAEAGQAFAGAFADQAHADAHAAIAPgCQAHgCAFgDIAAAYQgHAEgIABIgRACQgMAAgMgFg");
	this.shape_5.setTransform(73.4,12.2);
	this.shape_6 = new cjs.Shape();
	this.shape_6.graphics.f("#000000").s().p("AAVAwIgVgdIgUAdIggAAIAlgwIgjgvIAfAAIATAdIATgdIAgAAIgjAvIAlAwg");
	this.shape_6.setTransform(63.3,12.2);
	this.shape_7 = new cjs.Shape();
	this.shape_7.graphics.f("#000000").s().p("AgxBGIAAiLIBhAAIAAAaIhDAAIAAAeIA+AAIAAAZIg+AAIAAAgIBFAAIAAAag");
	this.shape_7.setTransform(52.2,10);
	this.shape_8 = new cjs.Shape();
	this.shape_8.graphics.f("#000000").s().p("AgOBGIAAhwIgrAAIAAgbIBzAAIAAAbIgrAAIAABwg");
	this.shape_8.setTransform(35.2,10);
	this.shape_9 = new cjs.Shape();
	this.shape_9.graphics.f("#000000").s().p("AgxBGIAAiLIBiAAIAAAbIhEAAIAAAhIA+AAIAAAaIg+AAIAAA1g");
	this.shape_9.setTransform(23.5,10);
	this.shape_10 = new cjs.Shape();
	this.shape_10.graphics.f("#000000").s().p("AgOBGIAAiLIAdAAIAACLg");
	this.shape_10.setTransform(14.1,10);
	this.shape_11 = new cjs.Shape();
	this.shape_11.graphics.f("#000000").s().p("AgMBFQgOgFgLgJQgKgIgHgOQgGgOAAgTQAAgSAGgOQAHgNAKgJQALgJAOgFQAMgEAPAAQALAAALACQALADAKAEIAAAdQgIgGgKgCQgKgDgLAAQgNAAgKAEQgLAFgHAKQgIAKAAAQQAAAOAFAJQAEAJAIAFQAHAGAHABQAIACAIAAIAJAAIAHgCIAAgxIAcAAIAABEQgKAFgMADIgXACQgPAAgNgEg");
	this.shape_11.setTransform(3.9,10);
	this.timeline.addTween(cjs.Tween.get({}).to({state:[{t:this.shape_11},{t:this.shape_10},{t:this.shape_9},{t:this.shape_8},{t:this.shape_7},{t:this.shape_6},{t:this.shape_5},{t:this.shape_4},{t:this.shape_3},{t:this.shape_2},{t:this.shape_1},{t:this.shape}]}).wait(1));
}).prototype = getMCSymbolPrototype(lib.OGiExchange, new cjs.Rectangle(-5,0,143.6,24), null);
(lib.OGiCloud = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f("#222222").s().p("AgfBAQgLgHgEgLQgGgMAAgOQAAgNAGgLQAEgLALgHQALgHAPgBQAKABAIAEQAIADAEAGIAAg2IAcAAIAACKIgZAAIAAgNQgEAGgIAFQgJAFgMABQgPgBgLgHgAgMgCQgFACgDAGQgDAHgBAHQABAIADAGQADAGAFAEQAGAEAGAAQAKAAAGgFQAHgEACgHIAAgXQgCgHgHgDQgGgFgKAAQgGAAgGAEg");
	this.shape.setTransform(95.6,10.1);
	this.shape_1 = new cjs.Shape();
	this.shape_1.graphics.f("#222222").s().p("AgdAsQgJgFgEgJQgFgJAAgLIAAg6IAcAAIAAA3QAAAJAFAEQAFAGAJgBQAGAAAFgDQAGgFADgEIAAg9IAcAAIAABeIgZAAIAAgMQgFAHgIAEQgIAEgKABQgNgBgIgFg");
	this.shape_1.setTransform(83.7,12.3);
	this.shape_2 = new cjs.Shape();
	this.shape_2.graphics.f("#222222").s().p("AgZAtQgMgFgIgMQgHgLAAgRQAAgQAHgLQAIgMAMgFQAMgGANAAQAOAAAMAGQAMAFAHAMQAIALAAAQQAAARgIALQgHAMgMAFQgMAGgOAAQgNAAgMgGgAgSgSQgFAIAAAKQAAALAFAIQAHAGALABQAMgBAGgGQAHgIgBgLQABgKgHgIQgGgGgMgBQgLABgHAGg");
	this.shape_2.setTransform(71.9,12.2);
	this.shape_3 = new cjs.Shape();
	this.shape_3.graphics.f("#222222").s().p("AgNBJIAAiRIAbAAIAACRg");
	this.shape_3.setTransform(63.4,9.7);
	this.shape_4 = new cjs.Shape();
	this.shape_4.graphics.f("#222222").s().p("AgJBFQgNgFgLgJQgLgIgGgNQgHgOAAgTQAAgRAHgOQAGgOALgKQAKgJAOgFQAMgEAOAAQALAAAKACQAKACAJAFIAAAdQgHgGgJgDQgJgCgKAAQgMAAgLAEQgLAGgHAKQgHAKAAAQQAAAQAHAKQAHAJALAGQALAEAMAAQALAAAJgDQAKgDAGgFIAAAdQgJAEgKADQgKACgLAAQgPAAgMgEg");
	this.shape_4.setTransform(54.2,10);
	this.shape_5 = new cjs.Shape();
	this.shape_5.graphics.f("#222222").s().p("AgOBGIAAhwIgrAAIAAgbIBzAAIAAAbIgrAAIAABwg");
	this.shape_5.setTransform(37.2,10);
	this.shape_6 = new cjs.Shape();
	this.shape_6.graphics.f("#222222").s().p("AgxBGIAAiLIBiAAIAAAbIhDAAIAAAhIA+AAIAAAaIg+AAIAAA1g");
	this.shape_6.setTransform(25.5,10);
	this.shape_7 = new cjs.Shape();
	this.shape_7.graphics.f("#222222").s().p("AgOBGIAAiLIAdAAIAACLg");
	this.shape_7.setTransform(16.1,10);
	this.shape_8 = new cjs.Shape();
	this.shape_8.graphics.f("#222222").s().p("AgMBFQgOgFgLgJQgKgIgHgOQgGgOAAgTQAAgSAGgOQAHgNAKgJQALgJAOgFQAMgEAPAAQALAAALACQALADAKAEIAAAdQgIgGgKgCQgKgDgLAAQgNAAgKAEQgLAFgHAKQgIAKAAAQQAAAOAFAJQAEAJAIAFQAHAGAHABQAIACAIAAIAJAAIAHgCIAAgxIAcAAIAABEQgKAFgMADIgXACQgPAAgNgEg");
	this.shape_8.setTransform(5.9,10);
	this.timeline.addTween(cjs.Tween.get({}).to({state:[{t:this.shape_8},{t:this.shape_7},{t:this.shape_6},{t:this.shape_5},{t:this.shape_4},{t:this.shape_3},{t:this.shape_2},{t:this.shape_1},{t:this.shape}]}).wait(1));
}).prototype = getMCSymbolPrototype(lib.OGiCloud, new cjs.Rectangle(-3,0,107.3,24), null);
(lib.John = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f("#222222").s().p("AAUAxIAAg3QAAgJgFgEQgGgGgIAAQgGABgGADQgFAFgDAEIAAA9IgcAAIAAheIAZAAIAAAMQAFgHAIgEQAIgEAKgBQAMABAJAFQAJAFAEAJQAFAJAAALIAAA6g");
	this.shape.setTransform(39.9,12);
	this.shape_1 = new cjs.Shape();
	this.shape_1.graphics.f("#222222").s().p("AAUBGIAAg4QAAgKgFgEQgGgEgIAAQgGAAgGAEQgFADgDAFIAAA+IgcAAIAAiLIAcAAIAAA1QAFgGAHgDQAHgDAJAAQAMAAAJAFQAJAGAEAJQAFAIAAAKIAAA8g");
	this.shape_1.setTransform(28.2,10);
	this.shape_2 = new cjs.Shape();
	this.shape_2.graphics.f("#222222").s().p("AgZAtQgMgFgIgMQgHgLAAgRQAAgQAHgLQAIgMAMgFQAMgGANAAQAOAAAMAGQAMAFAHAMQAIALAAAQQAAARgIALQgHAMgMAFQgMAGgOAAQgNAAgMgGgAgSgSQgFAIgBAKQABALAFAIQAHAGALABQAMgBAGgGQAHgIAAgLQAAgKgHgIQgGgGgMgBQgLABgHAGg");
	this.shape_2.setTransform(16.3,12.2);
	this.shape_3 = new cjs.Shape();
	this.shape_3.graphics.f("#222222").s().p("AgaBFQgKgCgGgDIAAgcQAGAEAHACQAIACAIAAQAHAAAGgCQAFgCAFgEQADgFAAgIIAAhCIgkAAIAAgbIBCAAIAABhQAAAQgHAKQgHAKgLAEQgMAEgMAAQgKAAgKgCg");
	this.shape_3.setTransform(4.6,10.1);
	this.timeline.addTween(cjs.Tween.get({}).to({state:[{t:this.shape_3},{t:this.shape_2},{t:this.shape_1},{t:this.shape}]}).wait(1));
}).prototype = getMCSymbolPrototype(lib.John, new cjs.Rectangle(-2,0,49.9,24), null);
(lib.GitHubProject = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f("#222222").s().p("AgDAzQgGgDgEgGQgDgFgBgJIAAgiIgMAAIAAgTIAMAAIAAgWIAWgFIAAAbIAXAAIAAATIgXAAIAAAdQAAAGADADQACACAHAAIAHAAIAGgCIAAASIgJACIgLABQgHAAgGgCg");
	this.shape.setTransform(50.5,27.5);
	this.shape_1 = new cjs.Shape();
	this.shape_1.graphics.f("#222222").s().p("AgLAkQgJgEgHgJQgGgIAAgOQAAgKAEgIQADgIAHgFQAGgFAIgDQAGgCAJAAIAMABQAGACAFADIAAATIgKgEQgFgCgFAAQgGAAgGADQgEACgDAEQgEAFAAAHQAAAHAEAFQADAFAEACQAFACAHAAQAFAAAGgBIAKgEIAAATIgMAEIgOACQgKAAgJgFg");
	this.shape_1.setTransform(43.2,28.7);
	this.shape_2 = new cjs.Shape();
	this.shape_2.graphics.f("#222222").s().p("AgPAkQgKgFgGgJQgHgJAAgNQAAgKAEgIQAEgHAGgFQAGgFAGgDQAHgCAGAAQAMAAAIAEQAIAFAEAHQAFAHABAIQABAIgCAIIg1AAQABAGAEADQAEAEAGABQAEACAHAAIAMgBIALgEIAAASQgFACgHABIgQACQgLAAgKgFgAgGgVQgEACgDAEQgCADAAAGIAhAAIgBgHQgBgEgEgDQgDgDgHAAQgEAAgEACg");
	this.shape_2.setTransform(34.9,28.7);
	this.shape_3 = new cjs.Shape();
	this.shape_3.graphics.f("#222222").s().p("AgOBMIgHgCIAAgTIAFABIADAAQAFABADgDQADgCAAgGIAAhTIAWAAIAABXQgBAKgEAFQgDAGgHADQgFACgGAAIgIAAgAAAg1QgDgDgBgHQABgGADgDQADgDAGAAQAEAAAFADQADADAAAGQAAAHgDADQgFADgEAAQgGAAgDgDg");
	this.shape_3.setTransform(27.7,28.7);
	this.shape_4 = new cjs.Shape();
	this.shape_4.graphics.f("#222222").s().p("AgUAkQgJgFgGgJQgGgJgBgNQABgNAGgJQAGgJAJgEQAKgFAKAAQALAAAKAFQAKAEAFAJQAHAJAAANQAAANgHAJQgFAJgKAFQgKAFgLAAQgKAAgKgFgAgOgOQgEAGAAAIQAAAJAEAGQAGAFAIABQAJgBAGgFQAFgGAAgJQAAgIgFgGQgGgGgJAAQgIAAgGAGg");
	this.shape_4.setTransform(21.7,28.7);
	this.shape_5 = new cjs.Shape();
	this.shape_5.graphics.f("#222222").s().p("AgYAnIAAhMIATAAIAAAMQAFgHAHgDQAIgEAKABIAAAVQgGgBgFACQgGABgEADQgEADgCAEIAAAsg");
	this.shape_5.setTransform(14.1,28.6);
	this.shape_6 = new cjs.Shape();
	this.shape_6.graphics.f("#222222").s().p("AgsA4IAAhvIAqAAQANAAALADQAKAEAHAIQAGAJAAAOQAAAOgGAHQgHAJgKADQgLADgNAAIgSAAIAAAlgAgUgBIATAAQAFAAAFgBQAGgCADgDQADgEAAgGQAAgHgDgDQgDgEgGgCQgFgBgFAAIgTAAg");
	this.shape_6.setTransform(5.7,27);
	this.shape_7 = new cjs.Shape();
	this.shape_7.graphics.f("#222222").s().p("AgLA1QgHgEgEgFIAAALIgTAAIAAhvIAVAAIAAArQAEgEAGgDQAHgDAIAAQAMAAAIAGQAJAFAEAJQAEAJAAAKQAAALgEAJQgEAJgJAGQgIAGgMAAQgJAAgHgEgAgMgBQgFADgDAFIAAASQADAGAFADQAFAEAHAAQAGAAAFgDQAEgDACgFQACgFABgGQgBgGgCgFQgCgFgEgCQgFgCgGgBQgHABgFADg");
	this.shape_7.setTransform(49,8.1);
	this.shape_8 = new cjs.Shape();
	this.shape_8.graphics.f("#222222").s().p("AgXAjQgHgEgEgHQgDgHAAgJIAAgvIAWAAIAAAsQAAAIAEAEQAEADAHAAQAFAAAEgDIAHgGIAAgyIAWAAIAABMIgTAAIAAgKQgFAGgGADQgHADgHABQgKgBgHgEg");
	this.shape_8.setTransform(39,9.8);
	this.shape_9 = new cjs.Shape();
	this.shape_9.graphics.f("#222222").s().p("AAaA4IAAgtIgyAAIAAAtIgYAAIAAhvIAYAAIAAAtIAyAAIAAgtIAXAAIAABvg");
	this.shape_9.setTransform(28.2,8);
	this.shape_10 = new cjs.Shape();
	this.shape_10.graphics.f("#222222").s().p("AgDAzQgGgDgEgGQgDgFgBgKIAAghIgMAAIAAgTIAMAAIAAgWIAWgGIAAAcIAXAAIAAATIgXAAIAAAdQAAAGACADQAEADAFgBIAIAAIAHgCIAAASIgKACIgLABQgIAAgFgCg");
	this.shape_10.setTransform(18.7,8.5);
	this.shape_11 = new cjs.Shape();
	this.shape_11.graphics.f("#222222").s().p("AgKA5IAAhMIAVAAIAABMgAgIgiQgEgDAAgHQAAgGAEgDQAEgEAEABQAFgBAEAEQAEADAAAGQAAAHgEADQgEADgFAAQgEAAgEgDg");
	this.shape_11.setTransform(13.3,7.8);
	this.shape_12 = new cjs.Shape();
	this.shape_12.graphics.f("#222222").s().p("AgKA3QgKgEgJgHQgIgHgGgLQgFgLAAgPQAAgOAFgMQAGgLAIgHQAJgHAKgDQAKgEAMABQAJAAAJABQAJACAIAEIAAAXQgHgFgIgCQgJgCgIAAQgKAAgIAEQgJADgFAJQgHAIABAMQAAALADAHQAEAHAFAFQAGAEAGABQAHACAGAAIAHgBIAFgBIAAgnIAXAAIAAA2QgIAEgKACIgSACQgNAAgKgDg");
	this.shape_12.setTransform(5.5,8);
	this.timeline.addTween(cjs.Tween.get({}).to({state:[{t:this.shape_12},{t:this.shape_11},{t:this.shape_10},{t:this.shape_9},{t:this.shape_8},{t:this.shape_7},{t:this.shape_6},{t:this.shape_5},{t:this.shape_4},{t:this.shape_3},{t:this.shape_2},{t:this.shape_1},{t:this.shape}]}).wait(1));
}).prototype = getMCSymbolPrototype(lib.GitHubProject, new cjs.Rectangle(-2,-0.4,61.5,39), null);
(lib.GIFT_2 = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f("#000000").s().p("AgLA4IAAhZIgiAAIAAgWIBbAAIAAAWIgiAAIAABZg");
	this.shape.setTransform(30.5,8);
	this.shape_1 = new cjs.Shape();
	this.shape_1.graphics.f("#000000").s().p("AgmA4IAAhvIBNAAIAAAWIg2AAIAAAZIAyAAIAAAWIgyAAIAAAqg");
	this.shape_1.setTransform(21.2,8);
	this.shape_2 = new cjs.Shape();
	this.shape_2.graphics.f("#000000").s().p("AgLA4IAAhvIAXAAIAABvg");
	this.shape_2.setTransform(13.7,8);
	this.shape_3 = new cjs.Shape();
	this.shape_3.graphics.f("#000000").s().p("AgKA3QgKgEgJgHQgIgHgGgLQgFgLAAgPQAAgOAFgMQAGgLAIgHQAJgHAKgDQAKgEAMABQAJAAAJABQAJACAIAEIAAAXQgHgFgIgCQgJgCgIAAQgKAAgIAEQgJADgFAJQgHAIABAMQAAALADAHQAEAHAFAFQAGAEAGABQAHACAGAAIAHgBIAFgBIAAgnIAXAAIAAA2QgIAEgKACIgSACQgNAAgKgDg");
	this.shape_3.setTransform(5.5,8);
	this.timeline.addTween(cjs.Tween.get({}).to({state:[{t:this.shape_3},{t:this.shape_2},{t:this.shape_1},{t:this.shape}]}).wait(1));
}).prototype = getMCSymbolPrototype(lib.GIFT_2, new cjs.Rectangle(-2,-0.4,39.6,20), null);
(lib.GIFT_1 = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f("#000000").s().p("AgLA4IAAhZIgiAAIAAgWIBbAAIAAAWIgiAAIAABZg");
	this.shape.setTransform(30.5,8);
	this.shape_1 = new cjs.Shape();
	this.shape_1.graphics.f("#000000").s().p("AgmA4IAAhvIBNAAIAAAWIg2AAIAAAZIAyAAIAAAWIgyAAIAAAqg");
	this.shape_1.setTransform(21.2,8);
	this.shape_2 = new cjs.Shape();
	this.shape_2.graphics.f("#000000").s().p("AgLA4IAAhvIAXAAIAABvg");
	this.shape_2.setTransform(13.7,8);
	this.shape_3 = new cjs.Shape();
	this.shape_3.graphics.f("#000000").s().p("AgKA3QgKgEgJgHQgIgHgGgLQgFgLAAgPQAAgOAFgMQAGgLAIgHQAJgHAKgDQAKgEAMABQAJAAAJABQAJACAIAEIAAAXQgHgFgIgCQgJgCgIAAQgKAAgIAEQgJADgFAJQgHAIABAMQAAALADAHQAEAHAFAFQAGAEAGABQAHACAGAAIAHgBIAFgBIAAgnIAXAAIAAA2QgIAEgKACIgSACQgNAAgKgDg");
	this.shape_3.setTransform(5.5,8);
	this.timeline.addTween(cjs.Tween.get({}).to({state:[{t:this.shape_3},{t:this.shape_2},{t:this.shape_1},{t:this.shape}]}).wait(1));
}).prototype = getMCSymbolPrototype(lib.GIFT_1, new cjs.Rectangle(-2,-0.4,39.6,20), null);
(lib.GIFT_0 = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f("#000000").s().p("AgLA4IAAhaIgiAAIAAgVIBbAAIAAAVIgiAAIAABag");
	this.shape.setTransform(30.5,8);
	this.shape_1 = new cjs.Shape();
	this.shape_1.graphics.f("#000000").s().p("AgmA4IAAhvIBNAAIAAAVIg2AAIAAAbIAyAAIAAAUIgyAAIAAArg");
	this.shape_1.setTransform(21.2,8);
	this.shape_2 = new cjs.Shape();
	this.shape_2.graphics.f("#000000").s().p("AgLA4IAAhvIAXAAIAABvg");
	this.shape_2.setTransform(13.7,8);
	this.shape_3 = new cjs.Shape();
	this.shape_3.graphics.f("#000000").s().p("AgKA3QgKgEgJgHQgIgHgGgLQgFgLAAgPQAAgOAFgMQAGgLAIgHQAJgHAKgDQAKgEAMABQAJAAAJABQAJACAIAEIAAAXQgHgFgIgCQgJgCgIAAQgKAAgIAEQgJADgFAJQgHAIABAMQAAALADAHQAEAHAFAFQAGAEAGABQAHACAGAAIAHgBIAFgBIAAgnIAXAAIAAA2QgIAEgKACIgSACQgNAAgKgDg");
	this.shape_3.setTransform(5.5,8);
	this.timeline.addTween(cjs.Tween.get({}).to({state:[{t:this.shape_3},{t:this.shape_2},{t:this.shape_1},{t:this.shape}]}).wait(1));
}).prototype = getMCSymbolPrototype(lib.GIFT_0, new cjs.Rectangle(-2,-0.4,39.6,20), null);
(lib.GIFT = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f("#000000").s().p("AgLA4IAAhaIgiAAIAAgVIBbAAIAAAVIgiAAIAABag");
	this.shape.setTransform(30.5,8);
	this.shape_1 = new cjs.Shape();
	this.shape_1.graphics.f("#000000").s().p("AgmA4IAAhvIBNAAIAAAVIg2AAIAAAbIAyAAIAAAUIgyAAIAAArg");
	this.shape_1.setTransform(21.2,8);
	this.shape_2 = new cjs.Shape();
	this.shape_2.graphics.f("#000000").s().p("AgLA4IAAhvIAXAAIAABvg");
	this.shape_2.setTransform(13.7,8);
	this.shape_3 = new cjs.Shape();
	this.shape_3.graphics.f("#000000").s().p("AgKA3QgKgEgJgHQgIgHgGgLQgFgLAAgPQAAgOAFgMQAGgLAIgHQAJgHAKgDQAKgEAMABQAJAAAJABQAJACAIAEIAAAXQgHgFgIgCQgJgCgIAAQgKAAgIAEQgJADgFAJQgHAIABAMQAAALADAHQAEAHAFAFQAGAEAGABQAHACAGAAIAHgBIAFgBIAAgnIAXAAIAAA2QgIAEgKACIgSACQgNAAgKgDg");
	this.shape_3.setTransform(5.5,8);
	this.timeline.addTween(cjs.Tween.get({}).to({state:[{t:this.shape_3},{t:this.shape_2},{t:this.shape_1},{t:this.shape}]}).wait(1));
}).prototype = getMCSymbolPrototype(lib.GIFT, new cjs.Rectangle(-2,-0.4,39.6,20), null);
(lib.Dоthetask = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f("#FFFFFF").s().p("AgNBRQgGgFAAgKQAAgKAGgEQAGgGAHAAQAJAAAFAGQAGAEAAAKQAAAKgGAFQgFAFgJgBQgHABgGgFgAgOAZIgChuIAiAAIgCBug");
	this.shape.setTransform(133.3,26.9);
	this.shape_1 = new cjs.Shape();
	this.shape_1.graphics.f("#FFFFFF").s().p("AgYA2QgPgHgJgOQgJgNgBgUQABgPAFgMQAGgMAIgHQAJgHALgEQAKgDAJAAQASAAAMAHQAMAFAGALQAHALACAMQABAMgDANIhQAAQACAIAHAFQAFAFAJADQAHACAKAAQAKAAAJgCQAIgBAHgDIAAAaQgHADgLACQgKACgNAAQgSAAgPgHgAgKgfQgGACgEAGQgEAFAAAIIAzAAQAAgEgBgGQgDgGgFgEQgFgFgLABQgGAAgGADg");
	this.shape_1.setTransform(123.5,29.4);
	this.shape_2 = new cjs.Shape();
	this.shape_2.graphics.f("#FFFFFF").s().p("AglA7IAAhyIAeAAIAAARQAGgKALgGQAMgFAQABIAAAhQgJgCgJACQgIABgHAFQgFAEgEAHIAABDg");
	this.shape_2.setTransform(112.7,29.2);
	this.shape_3 = new cjs.Shape();
	this.shape_3.graphics.f("#FFFFFF").s().p("AgkA1QgKgGgFgLQgFgLAAgNIAAhGIAhAAIAABBQAAAMAGAGQAGAFAKAAQAIAAAGgEQAHgFAEgFIAAhKIAhAAIAAByIgdAAIAAgPQgHAIgKAFQgJAFgMAAQgPAAgLgGg");
	this.shape_3.setTransform(100.4,29.5);
	this.shape_4 = new cjs.Shape();
	this.shape_4.graphics.f("#FFFFFF").s().p("AgFBMQgJgEgGgIQgFgJgBgOIAAgzIgTAAIAAgcIATAAIAAgiIAhgHIAAApIAkAAIAAAcIgkAAIAAAsQgBAJAFAFQAFAEAJAAIAKgBIALgDIAAAbIgPADQgIACgIAAQgLAAgJgEg");
	this.shape_4.setTransform(88.3,27.5);
	this.shape_5 = new cjs.Shape();
	this.shape_5.graphics.f("#FFFFFF").s().p("AgpA5QgKgEgFgIQgGgIAAgMQABgKAEgIQAFgHAHgEQAHgEAJgCQAJgCAJAAIANABIANADIAAgFQABgJgIgFQgGgFgNAAQgLAAgLACQgLADgHAEIAAgdIATgGQAMgCANAAQAQAAANAFQAMAFAIALQAHAMAAATIAAAkQgBAEADACQADACADAAIADgBIADgBIAAAXIgJABIgKABQgIAAgHgCQgGgEgEgGQgJAGgKAEQgIAEgNAAQgMAAgIgEgAgPAJQgGABgDADQgDAEgBAGQAAAHAGADQAFAEAHAAQAIAAAFgCQAHgCAFgFIAAgSIgJgCIgJgBQgGAAgGACg");
	this.shape_5.setTransform(76.9,29.4);
	this.shape_6 = new cjs.Shape();
	this.shape_6.graphics.f("#FFFFFF").s().p("AgYA2QgPgHgJgOQgJgNgBgUQABgPAFgMQAGgMAIgHQAKgHAKgEQAKgDAJAAQASAAAMAHQAMAFAHALQAGALACAMQACAMgDANIhQAAQABAIAHAFQAFAFAJADQAHACAKAAQAKAAAIgCQAJgBAHgDIAAAaQgHADgLACQgLACgNAAQgRAAgPgHgAgKgfQgGACgEAGQgEAFAAAIIAyAAQABgEgCgGQgCgGgFgEQgFgFgLABQgGAAgGADg");
	this.shape_6.setTransform(63.5,29.4);
	this.shape_7 = new cjs.Shape();
	this.shape_7.graphics.f("#FFFFFF").s().p("AgaBWIAAhWIgUAAIAAgcIAUAAIAAgMQAAgRAHgKQAHgKAKgEQAJgEAMAAQAIAAAHACIANADIAAAcIgJgDIgLgCQgIAAgGAEQgGAEgBALIAAAKIAkAAIAAAcIgkAAIAABWg");
	this.shape_7.setTransform(52.4,26.5);
	this.shape_8 = new cjs.Shape();
	this.shape_8.graphics.f("#FFFFFF").s().p("AgbA6QgMgDgJgFIAAgcQAKAHAMACQALADALAAQAJABAFgCQAFgCAAgFQAAgFgGgDQgHgDgJgDIgTgHQgJgEgHgGQgGgHgBgMQABgOAGgIQAHgHALgEQALgDAMAAQAMAAAKACQALADAJAFIAAAbIgMgGIgOgEIgOgBIgHAAQgEABgCACQgDACAAAEQABAFAGAEIAPAFIAUAGQAJAFAHAFQAGAIABAMQgBAOgHAIQgHAHgMADQgMAEgNAAQgNAAgMgDg");
	this.shape_8.setTransform(36.3,29.4);
	this.shape_9 = new cjs.Shape();
	this.shape_9.graphics.f("#FFFFFF").s().p("AgQBWIAAhyIAhAAIAABygAgNg0QgFgFAAgKQAAgJAFgEQAGgFAHAAQAIAAAGAFQAFAEAAAJQAAAKgFAFQgGAFgIAAQgHAAgGgFg");
	this.shape_9.setTransform(27.3,26.5);
	this.shape_10 = new cjs.Shape();
	this.shape_10.graphics.f("#FFFFFF").s().p("AAYBUIAAhDQAAgLgGgGQgGgFgKAAQgIAAgHAFQgGADgEAGIAABLIgiAAIAAinIAiAAIAABAQAGgHAJgDQAIgFALAAQAPABAKAGQAKAGAGALQAFAKAAANIAABHg");
	this.shape_10.setTransform(17.2,26.7);
	this.shape_11 = new cjs.Shape();
	this.shape_11.graphics.f("#FFFFFF").s().p("AgFBMQgJgEgGgIQgGgJABgOIAAgzIgUAAIAAgcIAUAAIAAgiIAfgHIAAApIAlAAIAAAcIglAAIAAAsQABAJAEAFQAFAEAJAAIAKgBIALgDIAAAbIgPADQgIACgIAAQgLAAgJgEg");
	this.shape_11.setTransform(5,27.5);
	this.shape_12 = new cjs.Shape();
	this.shape_12.graphics.f("#FFFFFF").s().p("AglBNQgNgJgGgOQgHgNAAgQQAAgQAHgNQAGgOANgIQAMgJATAAQAMAAAKAEQAJAFAGAGIAAhBIAhAAIAACnIgdAAIAAgRQgGAIgKAGQgKAGgPABQgTgBgMgIgAgOgDQgHAEgEAHQgDAIgBAJQABAJADAHQAEAIAHAEQAGAEAJABQALgBAIgFQAHgGAEgIIAAgbQgEgIgHgEQgIgGgLAAQgJAAgGAEg");
	this.shape_12.setTransform(60.1,-1.9);
	this.shape_13 = new cjs.Shape();
	this.shape_13.graphics.f("#FFFFFF").s().p("AgYA2QgPgHgJgOQgJgNgBgUQABgPAFgMQAGgMAIgHQAJgHALgEQAKgDAJAAQASAAAMAHQAMAFAGALQAHALACAMQACAMgDANIhQAAQABAIAHAFQAFAFAJADQAHACAKAAQAKAAAIgCQAJgBAHgDIAAAaQgIADgKACQgKACgNAAQgSAAgPgHgAgKggQgGADgEAGQgDAFgBAIIAzAAQAAgEgCgGQgBgGgGgEQgFgFgLABQgGAAgGACg");
	this.shape_13.setTransform(46.5,0.6);
	this.shape_14 = new cjs.Shape();
	this.shape_14.graphics.f("#FFFFFF").s().p("AgYA2QgPgHgJgOQgJgNgBgUQABgPAFgMQAGgMAIgHQAKgHAKgEQAKgDAJAAQASAAAMAHQAMAFAHALQAGALACAMQACAMgDANIhQAAQABAIAHAFQAFAFAJADQAHACAKAAQAKAAAIgCQAJgBAHgDIAAAaQgHADgLACQgLACgNAAQgRAAgPgHgAgKggQgGADgEAGQgEAFAAAIIAyAAQABgEgCgGQgCgGgFgEQgFgFgLABQgGAAgGACg");
	this.shape_14.setTransform(33.3,0.6);
	this.shape_15 = new cjs.Shape();
	this.shape_15.graphics.f("#FFFFFF").s().p("AAYA7IAAhCQAAgLgHgGQgGgGgJAAQgIABgGAEQgIAFgDAFIAABKIgiAAIAAhyIAeAAIAAAPQAHgIAJgFQAKgFAMAAQAPAAAKAGQAKAGAGALQAFALABANIAABGg");
	this.shape_15.setTransform(19.7,0.4);
	this.shape_16 = new cjs.Shape();
	this.shape_16.graphics.f("#FFFFFF").s().p("AgRBUIAAinIAjAAIAACng");
	this.shape_16.setTransform(3.6,-2.1);
	this.timeline.addTween(cjs.Tween.get({}).to({state:[{t:this.shape_16},{t:this.shape_15},{t:this.shape_14},{t:this.shape_13},{t:this.shape_12},{t:this.shape_11},{t:this.shape_10},{t:this.shape_9},{t:this.shape_8},{t:this.shape_7},{t:this.shape_6},{t:this.shape_5},{t:this.shape_4},{t:this.shape_3},{t:this.shape_2},{t:this.shape_1},{t:this.shape}]}).wait(1));
}).prototype = getMCSymbolPrototype(lib.Dоthetask, new cjs.Rectangle(-2,-13.7,140.8,56.8), null);
(lib.Bob_0 = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f("#222222").s().p("AgUAtQgNgFgHgMQgIgLAAgRQAAgNAFgJQAEgKAIgGQAHgGAJgDQAIgDAIAAQAOAAAKAGQAKAEAGAJQAGAJABAKQABALgCAKIhDAAQACAHAFAFQAFAEAHACQAGACAIAAQAIAAAIgBIANgFIAAAWIgQAEIgTACQgPAAgMgGgAgIgaQgGACgDAFQgDAFAAAGIAqAAQAAgDgBgFQgCgFgEgDQgFgFgIAAQgFAAgFADg");
	this.shape.setTransform(39.5,13.2);
	this.shape_1 = new cjs.Shape();
	this.shape_1.graphics.f("#222222").s().p("AgOAuQgMgGgIgKQgHgMAAgQQAAgNAEgLQAFgJAIgHQAIgGAJgDQAJgDAKAAQAIAAAHABQAIACAGAEIAAAYQgFgDgGgCQgHgCgHAAQgIAAgHADQgFADgFAGQgEAFAAAJQAAAJAEAGQAFAGAFADQAHADAHAAIAPgCQAHgCAFgDIAAAZQgHACgIACIgRACQgMAAgMgFg");
	this.shape_1.setTransform(29.1,13.2);
	this.shape_2 = new cjs.Shape();
	this.shape_2.graphics.f("#222222").s().p("AgNBIIAAhfIAbAAIAABfgAgKgrQgFgEAAgIQAAgIAFgEQAEgEAGAAQAHAAAFAEQAEAEAAAIQAAAIgEAEQgFAEgHAAQgGAAgEgEg");
	this.shape_2.setTransform(21.6,10.8);
	this.shape_3 = new cjs.Shape();
	this.shape_3.graphics.f("#222222").s().p("AgNBJIAAiRIAbAAIAACRg");
	this.shape_3.setTransform(16.4,10.7);
	this.shape_4 = new cjs.Shape();
	this.shape_4.graphics.f("#222222").s().p("AAqBGIgKgaIg/AAIgKAaIgfAAIA5iLIAfAAIA5CLgAAXATIgUgxIgBgFIgCgGIAAAGIgCAFIgTAxIAsAAg");
	this.shape_4.setTransform(6.4,11);
	this.timeline.addTween(cjs.Tween.get({}).to({state:[{t:this.shape_4},{t:this.shape_3},{t:this.shape_2},{t:this.shape_1},{t:this.shape}]}).wait(1));
}).prototype = getMCSymbolPrototype(lib.Bob_0, new cjs.Rectangle(-3,1,50.2,24), null);
(lib.Bob = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f("#222222").s().p("AgPBCQgIgFgFgGIAAANIgYAAIAAiKIAbAAIAAA2QAFgGAIgDQAIgEAKgBQAPABALAHQAKAHAFALQAGALAAANQAAAOgGAMQgFALgKAHQgLAHgPABQgMgBgJgFgAgQgBQgFADgEAHIAAAXQAEAHAFAEQAHAFAJAAQAIAAAFgEQAGgEADgGQADgGAAgIQAAgHgDgHQgDgGgGgCQgFgEgIAAQgJAAgHAFg");
	this.shape.setTransform(32.1,10.1);
	this.shape_1 = new cjs.Shape();
	this.shape_1.graphics.f("#222222").s().p("AgZAtQgMgFgHgMQgIgLAAgRQAAgQAIgLQAHgMAMgFQAMgGANAAQAOAAAMAGQAMAFAIAMQAGALABAQQgBARgGALQgIAMgMAFQgMAGgOAAQgNAAgMgGgAgRgSQgHAIAAAKQAAALAHAIQAGAGALABQAMgBAHgGQAFgIABgLQgBgKgFgIQgHgGgMgBQgLABgGAGg");
	this.shape_1.setTransform(19.7,12.2);
	this.shape_2 = new cjs.Shape();
	this.shape_2.graphics.f("#222222").s().p("Ag4BGIAAiLIA7AAQAXAAANAIQANAKAAARQAAAMgGAIQgGAIgJADQAHACAGADQAGAEAEAIQADAGAAALQAAALgEAJQgFAHgJAEQgIAFgKACIgTABgAgbAtIAdAAIANgBQAGgBADgEQADgEAAgIQAAgGgDgEQgDgEgFgCQgGgBgGgBIgfAAgAgbgMIAdAAQAKgBAFgEQAFgEABgHQgBgIgFgFQgGgEgKABIgcAAg");
	this.shape_2.setTransform(7.3,10);
	this.timeline.addTween(cjs.Tween.get({}).to({state:[{t:this.shape_2},{t:this.shape_1},{t:this.shape}]}).wait(1));
}).prototype = getMCSymbolPrototype(lib.Bob, new cjs.Rectangle(-2,0,42.3,24), null);
(lib._50 = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f("#222222").s().p("AgsBKIBIiTIASAAIhICTgAAdA+QgHgDgFgIQgEgGAAgLQAAgJAEgIQAFgGAHgEQAIgDAIAAQAJAAAHADQAIAEAEAGQAFAIAAAJQAAALgFAGQgEAIgIADQgHADgJABQgIgBgIgDgAAkAaQgDADAAAFQAAAGADADQADAEAGAAQAHAAADgEQADgDAAgGQAAgFgDgDQgDgEgHAAQgGAAgDAEgAg8gGQgHgEgFgGQgEgIgBgJQABgLAEgGQAFgIAHgDQAHgDAJgBQAJABAHADQAIADAEAIQAEAGABALQgBAJgEAIQgEAGgIAEQgHADgJAAQgJAAgHgDgAg1gqQgDADAAAGQAAAFADADQADADAGABQAHgBADgDQADgDgBgFQABgGgDgDQgDgEgHAAQgGAAgDAEg");
	this.shape.setTransform(31.6,9);
	this.shape_1 = new cjs.Shape();
	this.shape_1.graphics.f("#222222").s().p("AgfA3QgMgIgGgPQgGgOAAgSQAAgRAGgOQAGgPAMgIQANgIASgBQAUABAMAIQAMAIAGAPQAGAOAAARQAAASgGAOQgGAPgMAIQgMAJgUAAQgSAAgNgJgAgVgdQgHAKAAATQAAAUAHAKQAHAKAOAAQAPAAAHgKQAHgKAAgUQAAgTgHgKQgHgKgPAAQgOAAgHAKg");
	this.shape_1.setTransform(17,9.2);
	this.shape_2 = new cjs.Shape();
	this.shape_2.graphics.f("#222222").s().p("AgaA9QgKgDgJgEIAAgZQAIAFAKADQAJACAKAAQAIAAAFgCQAGgCAEgEQADgEABgGQAAgIgIgFQgIgEgNgBIgPABQgIACgIADIAEhGIBNAAIAAAWIg0AAIgCAYIAIgBIAHAAQAMAAAKADQAKAFAGAIQAGAIABANQgBAPgHAJQgHAJgMAEQgLAEgNABQgLAAgKgCg");
	this.shape_2.setTransform(5.4,9.3);
	this.timeline.addTween(cjs.Tween.get({}).to({state:[{t:this.shape_2},{t:this.shape_1},{t:this.shape}]}).wait(1));
}).prototype = getMCSymbolPrototype(lib._50, new cjs.Rectangle(-2,-0.2,44.1,22), null);
(lib._30 = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f("#222222").s().p("AgsBKIBIiTIASAAIhICTgAAdA+QgHgDgFgIQgEgGAAgLQAAgJAEgIQAFgGAHgEQAIgDAIAAQAJAAAHADQAIAEAEAGQAFAIAAAJQAAALgFAGQgEAIgIADQgHADgJABQgIgBgIgDgAAkAaQgDADAAAFQAAAGADADQADAEAGAAQAHAAADgEQADgDAAgGQAAgFgDgDQgDgEgHAAQgGAAgDAEgAg8gGQgHgEgFgGQgEgIgBgJQABgLAEgGQAFgIAHgDQAHgDAJgBQAJABAHADQAIADAEAIQAEAGABALQgBAJgEAIQgEAGgIAEQgHADgJAAQgJAAgHgDgAg1gqQgDADAAAGQAAAFADADQADADAGABQAHgBADgDQADgDgBgFQABgGgDgDQgDgEgHAAQgGAAgDAEg");
	this.shape.setTransform(31.7,9);
	this.shape_1 = new cjs.Shape();
	this.shape_1.graphics.f("#222222").s().p("AgfA3QgMgIgGgPQgGgOAAgSQAAgRAGgOQAGgPAMgIQANgIASgBQATABANAIQAMAIAGAPQAGAOAAARQAAASgGAOQgGAPgMAIQgNAJgTAAQgSAAgNgJgAgVgdQgHAKAAATQAAAUAHAKQAHAKAOAAQAPAAAHgKQAHgKAAgUQAAgTgHgKQgHgKgPAAQgOAAgHAKg");
	this.shape_1.setTransform(17.1,9.2);
	this.shape_2 = new cjs.Shape();
	this.shape_2.graphics.f("#222222").s().p("AgYA+QgLgCgKgFIAAgZQAKAGAKACQAKACALAAQAGAAAFgCQAGgBADgEQAEgDAAgGQAAgIgGgDQgGgDgIAAIgUAAIAAgWIARAAQAIAAAFgDQAFgEAAgGQAAgHgGgDQgFgEgKAAQgJAAgJADQgJACgKAGIAAgZQAJgFAKgCQAKgDALAAQAMAAAKAEQAKAEAGAHQAFAIABALQgBAKgEAHQgFAGgJADQAGACAGADQAFAEADAGQAEAHAAAJQgBANgGAIQgHAIgLADQgMAEgLAAQgMAAgKgCg");
	this.shape_2.setTransform(5.4,9.2);
	this.timeline.addTween(cjs.Tween.get({}).to({state:[{t:this.shape_2},{t:this.shape_1},{t:this.shape}]}).wait(1));
}).prototype = getMCSymbolPrototype(lib._30, new cjs.Rectangle(-2,-0.2,44.3,22), null);
(lib._20 = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f("#222222").s().p("AgsBKIBIiTIASAAIhICTgAAdA+QgHgDgFgIQgEgGAAgLQAAgJAEgIQAFgGAHgEQAIgDAIAAQAJAAAHADQAIAEAEAGQAFAIAAAJQAAALgFAGQgEAIgIADQgHADgJABQgIgBgIgDgAAkAaQgDADAAAFQAAAGADADQADAEAGAAQAHAAADgEQADgDAAgGQAAgFgDgDQgDgEgHAAQgGAAgDAEgAg8gGQgHgEgFgGQgEgIgBgJQABgLAEgGQAFgIAHgDQAHgDAJgBQAJABAHADQAIADAEAIQAEAGABALQgBAJgEAIQgEAGgIAEQgHADgJAAQgJAAgHgDgAg1gqQgDADAAAGQAAAFADADQADADAGABQAHgBADgDQADgDgBgFQABgGgDgDQgDgEgHAAQgGAAgDAEg");
	this.shape.setTransform(31.7,9);
	this.shape_1 = new cjs.Shape();
	this.shape_1.graphics.f("#222222").s().p("AgfA3QgMgIgGgPQgGgOAAgSQAAgRAGgOQAGgPAMgIQANgIASgBQATABANAIQAMAIAGAPQAGAOAAARQAAASgGAOQgGAPgMAIQgNAJgTAAQgSAAgNgJgAgVgdQgHAKAAATQAAAUAHAKQAHAKAOAAQAPAAAHgKQAHgKAAgUQAAgTgHgKQgHgKgPAAQgOAAgHAKg");
	this.shape_1.setTransform(17.1,9.2);
	this.shape_2 = new cjs.Shape();
	this.shape_2.graphics.f("#222222").s().p("AgtA/IAAgMQABgMADgHQADgJAHgFQAGgGAGgFIAPgHIAKgHIAJgIQADgEAAgFQAAgHgFgEQgGgDgIAAQgJAAgLAEQgKADgJAIIAAgZQAJgHAKgEQALgDAKAAQANAAAKAFQAKADAGAJQAGAHAAAMQAAALgFAIQgFAHgIAGIgPALIgNAIQgGADgEAEQgDADAAAEIA8AAIAAAYg");
	this.shape_2.setTransform(5.3,9.1);
	this.timeline.addTween(cjs.Tween.get({}).to({state:[{t:this.shape_2},{t:this.shape_1},{t:this.shape}]}).wait(1));
}).prototype = getMCSymbolPrototype(lib._20, new cjs.Rectangle(-2,-0.2,44.3,22), null);
(lib._1 = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f("#222222").s().p("AgMBeIAAgYQgLgBgLgDQgKgDgIgFIAAgdQAMAJANADQANADAMABQALAAAHgEQAGgDAAgHQAAgHgFgEQgGgDgIgDIgRgFQgKgDgIgFQgJgDgFgIQgFgHgBgNQABgMAFgIQAFgIAJgFQAIgEAMgCIAAgYIAVAAIAAAYQAKABAJACQAJADAHAEIAAAcQgJgHgLgDQgLgCgMAAQgLAAgFADQgGADAAAGQAAAHAGADQAFADAJADIARAGQAJADAJAEQAIADAGAJQAFAHAAAMQAAAOgGAJQgGAJgKAEQgKAFgMABIAAAXg");
	this.shape.setTransform(6.2,10.2);
	this.timeline.addTween(cjs.Tween.get(this.shape).wait(1));
}).prototype = getMCSymbolPrototype(lib._1, new cjs.Rectangle(-2,0,16.3,24), null);
(lib._0 = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f("#000000").s().p("AgMBeIAAgYQgLgBgLgDQgKgDgIgFIAAgcQAMAHANAEQANAEAMgBQALAAAHgCQAGgDAAgIQAAgGgFgEQgGgEgIgCIgRgGQgKgDgIgFQgJgEgFgHQgFgIgBgMQABgMAFgIQAFgIAJgFQAIgFAMgBIAAgYIAVAAIAAAYQAKABAJADQAJACAHAEIAAAcQgJgGgLgDQgLgEgMAAQgLAAgFAEQgGADAAAHQAAAFAGAEQAFAEAJACIARAFQAJADAJAFQAIAEAGAHQAFAIAAANQAAAOgGAIQgGAJgKAEQgKAEgMABIAAAYg");
	this.shape.setTransform(6.2,10.2);
	this.timeline.addTween(cjs.Tween.get(this.shape).wait(1));
}).prototype = getMCSymbolPrototype(lib._0, new cjs.Rectangle(-2,0,16.3,24), null);
(lib.Symbol = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f("#222222").s().p("AgMBeIAAgYQgLgBgLgDQgKgDgIgFIAAgcQAMAHANAEQANAEAMgBQALAAAHgCQAGgDAAgIQAAgGgFgEQgGgEgIgCIgRgGQgKgDgIgFQgJgEgFgHQgFgIgBgMQABgMAFgIQAFgIAJgFQAIgFAMgBIAAgYIAVAAIAAAYQAKABAJADQAJACAHAEIAAAcQgJgGgLgDQgLgEgMAAQgLAAgFAEQgGADAAAHQAAAFAGAEQAFAEAJACIARAFQAJADAJAFQAIAEAGAHQAFAIAAANQAAAOgGAIQgGAJgKAEQgKAEgMABIAAAYg");
	this.shape.setTransform(6.2,10.2);
	this.timeline.addTween(cjs.Tween.get(this.shape).wait(1));
}).prototype = getMCSymbolPrototype(lib.Symbol, new cjs.Rectangle(-2,0,16.3,24), null);
(lib.fdgfdg = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f().ls(["#FB5D67","#F27D38"],[0.075,1],0,0.5,0,-0.4).ss(3,2,0,4).p("AAAnhIAAPD");
	this.shape.setTransform(0,48.2);
	this.timeline.addTween(cjs.Tween.get(this.shape).wait(1));
}).prototype = getMCSymbolPrototype(lib.fdgfdg, new cjs.Rectangle(-1.5,-1.5,3,99.5), null);
(lib.f5g = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f("#E7E7E7").s().p("ArAAyQgVAAgPgOQgOgPAAgVQAAgUAOgOQAPgPAVAAIWBAAQAVAAAPAPQAOAOAAAUQAAAVgOAPQgPAOgVAAg");
	this.shape.setTransform(75.5,5);
	this.timeline.addTween(cjs.Tween.get(this.shape).wait(1));
}).prototype = getMCSymbolPrototype(lib.f5g, new cjs.Rectangle(0,0,151,10), null);
(lib.ergg = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f("#E7E7E7").s().p("ArAAyQgUAAgQgPQgOgPAAgUQAAgUAOgOQAQgPAUAAIWBAAQAUAAAPAPQAPAOAAAUQAAAUgPAPQgPAPgUAAg");
	this.shape.setTransform(75.5,5);
	this.timeline.addTween(cjs.Tween.get(this.shape).wait(1));
}).prototype = getMCSymbolPrototype(lib.ergg, new cjs.Rectangle(0,0,151,10), null);
(lib.eetert = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f().ls(["#FA635F","#F47741"],[0,1],-17,17,16.9,-16.9).ss(3,0,0,4).p("ACpipQBHBGAABjQAABjhHBHQhGBGhjAAQhiAAhGhGQhHhHAAhjQAAhjBHhGQBGhGBiAAQBjAABGBGg");
	this.shape.setTransform(24,24);
	this.shape_1 = new cjs.Shape();
	this.shape_1.graphics.f("#FFFFFF").s().p("AipCqQhGhHAAhjQAAhjBGhGQBHhGBiAAQBkAABFBGQBHBGAABjQAABjhHBHQhFBGhkAAQhiAAhHhGg");
	this.shape_1.setTransform(24,24);
	this.timeline.addTween(cjs.Tween.get({}).to({state:[{t:this.shape_1},{t:this.shape}]}).wait(1));
}).prototype = getMCSymbolPrototype(lib.eetert, new cjs.Rectangle(-1.5,-1.5,51,51), null);
(lib.eerfergg = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f("#F27D38").s().p("AhJgeIBrgUIAoBlg");
	this.shape.setTransform(7.5,5.1);
	this.timeline.addTween(cjs.Tween.get(this.shape).wait(1));
}).prototype = getMCSymbolPrototype(lib.eerfergg, new cjs.Rectangle(0,0,14.9,10.3), null);
(lib.e45tdg = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f().ls(["#FA635D","#F27D38"],[0.188,1],0,24.1,0,-23.9).ss(3,0,0,4).p("AAAjvQBjAABGBGQBHBGAABjQAABkhHBGQhGBGhjAAQhiAAhHhGQhGhGAAhkQAAhjBGhGQBHhGBiAAg");
	this.shape.setTransform(24,24);
	this.shape_1 = new cjs.Shape();
	this.shape_1.graphics.f("#FFFFFF").s().p("AipCqQhGhGAAhkQAAhjBGhGQBGhGBjAAQBjAABGBGQBHBGAABjQAABkhHBGQhGBGhjAAQhjAAhGhGg");
	this.shape_1.setTransform(24,24);
	this.timeline.addTween(cjs.Tween.get({}).to({state:[{t:this.shape_1},{t:this.shape}]}).wait(1));
}).prototype = getMCSymbolPrototype(lib.e45tdg, new cjs.Rectangle(-1.5,-1.5,51,51), null);
(lib._566hrhf = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f().ls(["#FA6061","#F47641"],[0,1],0,24,0,-24).ss(3,0,0,4).p("AAADwQBSAABAgyQBAgyAVhNQAJgeAAghQAAhjhHhGQhGhGhjAAQhiAAhHBGQhGBGAABjQAABkBGBGQBHBGBiAAg");
	this.shape.setTransform(24,24);
	this.shape_1 = new cjs.Shape();
	this.shape_1.graphics.f("#FFFFFF").s().p("AipCpQhGhGAAhjQAAhiBGhHQBGhGBjAAQBkAABFBGQBHBHAABiQAAAhgJAeQgVBNhAAyQhAAyhSAAQhjAAhGhHg");
	this.shape_1.setTransform(24,24);
	this.timeline.addTween(cjs.Tween.get({}).to({state:[{t:this.shape_1},{t:this.shape}]}).wait(1));
}).prototype = getMCSymbolPrototype(lib._566hrhf, new cjs.Rectangle(-1.5,-1.5,51,51), null);
(lib._56hgfhg = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f("#FC5E67").s().p("AhUgiICpAAIhVBFg");
	this.shape.setTransform(8.5,3.5);
	this.timeline.addTween(cjs.Tween.get(this.shape).wait(1));
}).prototype = getMCSymbolPrototype(lib._56hgfhg, new cjs.Rectangle(0,0,17,7), null);
(lib._45tgfbgfb = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f("#F27D38").s().p("AhUAjIBUhFIBVBFg");
	this.shape.setTransform(8.5,3.5);
	this.timeline.addTween(cjs.Tween.get(this.shape).wait(1));
}).prototype = getMCSymbolPrototype(lib._45tgfbgfb, new cjs.Rectangle(0,0,17,7), null);
(lib._45fdf = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.lf(["#38C2CF","#60BB97"],[0,1],112.5,-36.7,-106.7,41.1).s().p("Ai1OqQjogsjGh0Qi/huiFihQiEihg2i5Qg4i/Ali/QAli/B8icQB3iYC3hjQC3hkDbgfQDjghDnAuQDoAtDGByQC/BwCEChQCFCgA2C5QA3C/glC/QglC/h7CdQh4CYi3BiQi3BkjbAfQhfAOhfAAQiEAAiHgbg");
	this.shape.setTransform(115.6,96.5);
	this.shape_1 = new cjs.Shape();
	this.shape_1.graphics.f("#42C0BF").s().p("AjSBoIFNlQIBYHRg");
	this.shape_1.setTransform(196,160.7);
	this.timeline.addTween(cjs.Tween.get({}).to({state:[{t:this.shape_1},{t:this.shape}]}).wait(1));
}).prototype = getMCSymbolPrototype(lib._45fdf, new cjs.Rectangle(0,0,231.2,192.9), null);
(lib._7resgfd = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f().ls(["#FC5D67","#F27D38"],[0,1],0,0.6,0,-0.4).ss(3,2,0,4).p("AAAnVIAAOr");
	this.shape.setTransform(0,47);
	this.timeline.addTween(cjs.Tween.get(this.shape).wait(1));
}).prototype = getMCSymbolPrototype(lib._7resgfd, new cjs.Rectangle(-1.5,-1.5,3,97.1), null);
(lib._5ttrtrere = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f("#F27D38").s().p("AgagwIBoAfIibBCg");
	this.shape.setTransform(7.8,4.9);
	this.timeline.addTween(cjs.Tween.get(this.shape).wait(1));
}).prototype = getMCSymbolPrototype(lib._5ttrtrere, new cjs.Rectangle(0,0,15.7,9.8), null);
(lib._5ttrt = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f().ls(["#FA635F","#F47741"],[0,1],-16.9,17,17,-16.9).ss(3,0,0,4).p("ACqipQBGBGAABjQAABjhGBGQhGBHhkAAQhiAAhHhHQhGhGAAhjQAAhjBGhGQBHhGBiAAQBkAABGBGg");
	this.shape.setTransform(24,24);
	this.shape_1 = new cjs.Shape();
	this.shape_1.graphics.f("#FFFFFF").s().p("AipCpQhGhGAAhjQAAhjBGhGQBHhGBiAAQBkAABGBGQBGBGAABjQAABjhGBGQhGBHhkAAQhiAAhHhHg");
	this.shape_1.setTransform(24,24);
	this.timeline.addTween(cjs.Tween.get({}).to({state:[{t:this.shape_1},{t:this.shape}]}).wait(1));
}).prototype = getMCSymbolPrototype(lib._5ttrt, new cjs.Rectangle(-1.5,-1.5,51,51), null);
(lib._5ttrrh = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f().s("#FFFFFF").ss(5,0,0,4).p("AnUHhQhmgFhKhPQhKhQAAhnQAAhCAjg6QAkg6A8ghQAPgIAFgOQAGgPgGgOQgKgZAAgdQAAhBAxguQAxguBFAAQAeAAAbAJQAQAGAQgGQARgGAHgQQAvhdBdg4QBeg3BsAAQCUAABsBcQBrBcAPCKQAAAOALALQAKALAPACQBwASBKBWQBKBUAABuQAAB1hVBZQhVBZh5AIgAGxI2QCegLBthwQBthwAAiZQAAiEhWhpQhVhqiDggQgcigiChoQiDhoitAAQh9AAhuA8QhsA7g/BmQgYgEgZAAQhqAAhMBHQhLBHAABkQAAAYAGAaQhFAvgnBHQgnBIAABQQAACIBkBpQBjBoCJAHIOHAAg");
	this.shape.setTransform(80.9,56.6);
	this.shape_1 = new cjs.Shape();
	this.shape_1.graphics.lf(["#5FBB99","#38C2CF"],[0,1],0,78.9,0,-78.9).s().p("AnYI2QiJgHhjhoQhkhpAAiIQAAhQAnhIQAohHBEgvQgGgaABgYQAAhkBKhHQBMhHBqAAQAZAAAYAEQA/hmBtg7QBtg8B9AAQCtAACDBoQCCBoAcCgQCDAgBVBqQBWBpAACEQAACZhtBwQhtBwieALIgCAAgAoQjZQgwAuAABBQgBAdALAZQAFAOgFAPQgGAOgOAIQg9AhgkA6QgjA6AABCQAABnBKBQQBKBPBmAFIOBAAQB4gIBVhZQBVhZAAh1QAAhuhKhUQhKhWhwgSQgPgCgKgLQgKgLgBgOQgPiKhshcQhshciTAAQhtAAhdA3QhdA4guBdQgIAQgRAGQgQAGgQgGQgbgJgeAAQhFAAgxAug");
	this.shape_1.setTransform(80.9,56.6);
	this.timeline.addTween(cjs.Tween.get({}).to({state:[{t:this.shape_1},{t:this.shape}]}).wait(1));
}).prototype = getMCSymbolPrototype(lib._5ttrrh, new cjs.Rectangle(-2.5,-2.5,166.8,118.3), null);
(lib._5trgrh = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f().ls(["#FC5D67","#F27D38"],[0,1],0,0.6,0,-0.3).ss(3,2,0,4).p("AAAnWIAAOs");
	this.shape.setTransform(0,47.1);
	this.timeline.addTween(cjs.Tween.get(this.shape).wait(1));
}).prototype = getMCSymbolPrototype(lib._5trgrh, new cjs.Rectangle(-1.5,-1.5,3,97.1), null);
(lib._5tgh = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f().s("#FFFFFF").ss(3,0,0,4).p("AANBiQgVAWghAAQghAAgXgWQgXgXAAghQAAggAXgXQAXgXAhAAQAhAAAVAXQAYAXAAAgQAAAhgYAXgACtisQgJgJgNAAQgMAAgKAJIhgBhQghgWgpAAQg6AAgpApQgpAqAAA4QAAA5ApAqQApApA6AAQA5AAApgpQAjgjAFgyQAGgwgbgoIBhhhQAJgJAAgNQAAgMgJgJg");
	this.shape.setTransform(18.2,18.2);
	this.shape_1 = new cjs.Shape();
	this.shape_1.graphics.f("#38C1CE").s().p("AiMCNQgpgqAAg5QAAg4ApgqQApgpA6AAQApAAAhAWIBhhhQAJgJAMAAQANAAAJAJQAJAJAAAMQAAANgJAJIhgBhQAaAogGAwQgFAygjAjQgpApg5AAQg6AAgpgpgAhhgNQgWAXAAAgQAAAgAWAYQAYAWAgAAQAhAAAWgWQAXgYAAggQAAghgXgWQgWgWghAAQggAAgYAWg");
	this.shape_1.setTransform(18.2,18.2);
	this.timeline.addTween(cjs.Tween.get({}).to({state:[{t:this.shape_1},{t:this.shape}]}).wait(1));
}).prototype = getMCSymbolPrototype(lib._5tgh, new cjs.Rectangle(-1.5,-1.5,39.4,39.4), null);
(lib._5tergrt = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f("#E7E7E7").s().p("ArAAyQgVAAgPgPQgOgPAAgUQAAgUAOgPQAPgOAVAAIWBAAQAVAAAPAOQAOAPAAAUQAAAUgOAPQgPAPgVAAg");
	this.shape.setTransform(75.5,5);
	this.timeline.addTween(cjs.Tween.get(this.shape).wait(1));
}).prototype = getMCSymbolPrototype(lib._5tergrt, new cjs.Rectangle(0,0,151,10), null);
(lib._5ggfg = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f().ls(["#FA635F","#F47741"],[0,1],0,24,0,-24).ss(3,0,0,4).p("AAAjvQBjAABGBGQBHBGAABjQAABkhHBGQhGBGhjAAQhiAAhHhGQhGhGAAhkQAAhjBGhGQBHhGBiAAg");
	this.shape.setTransform(24,24);
	this.shape_1 = new cjs.Shape();
	this.shape_1.graphics.f("#FFFFFF").s().p("AipCpQhGhGAAhjQAAhiBGhHQBHhGBiAAQBjAABGBGQBHBHAABiQAABjhHBGQhGBHhjAAQhiAAhHhHg");
	this.shape_1.setTransform(24,24);
	this.timeline.addTween(cjs.Tween.get({}).to({state:[{t:this.shape_1},{t:this.shape}]}).wait(1));
}).prototype = getMCSymbolPrototype(lib._5ggfg, new cjs.Rectangle(-1.5,-1.5,51,51), null);
(lib._5etrt = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f().ls(["#FC5D67","#F27D38"],[0,1],0,64.6,0,-64.4).ss(3,2,0,4).p("AqE1PMAUJAqf");
	this.shape.setTransform(64.5,136);
	this.timeline.addTween(cjs.Tween.get(this.shape).wait(1));
}).prototype = getMCSymbolPrototype(lib._5etrt, new cjs.Rectangle(-2,-2,133,276), null);
(lib._4terdhh = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f().ls(["#F47741","#FA635F"],[0,1],0,24,0,-24).ss(3,0,0,4).p("AAAjvQBjAABGBGQBHBGAABjQAABkhHBGQhGBGhjAAQhiAAhHhGQhGhGAAhkQAAhjBGhGQBHhGBiAAg");
	this.shape.setTransform(24,24);
	this.shape_1 = new cjs.Shape();
	this.shape_1.graphics.f("#FFFFFF").s().p("AipCpQhGhGAAhjQAAhjBGhGQBGhGBjAAQBkAABGBGQBGBGAABjQAABjhGBGQhGBHhkAAQhjAAhGhHg");
	this.shape_1.setTransform(24,24);
	this.timeline.addTween(cjs.Tween.get({}).to({state:[{t:this.shape_1},{t:this.shape}]}).wait(1));
}).prototype = getMCSymbolPrototype(lib._4terdhh, new cjs.Rectangle(-1.5,-1.5,51,51), null);
(lib._4tdgdh = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.lf(["#3CC1C7","#5EBC9D"],[0,1],0,43.3,0,-43.2).s().p("AhZJnQgIAAgFgFQgFgGAAgHQAAgHAFgGQAFgFAIAAIFMAAIAAiqQAAgHAGgGQAFgFAHAAQAIAAAFAFQAFAGAAAHIAACqIBbAAQATAAAJgHQAKgIAAgSQAAgHgHghIgujpQgHgjgegTIgegNIhqgbIhwCDQgcAhglACQglACgegdQgEgEhyiHIh3AeQguASgJAuIguDqQgHAgAAAHQAAASAKAIQAJAHATAAIBbAAIAAiqQAAgHAGgGQAFgFAHAAQAIAAAFAFQAGAGAAAHIAACqIBDAAQAIAAAFAFQAFAGAAAHQAAAHgFAGQgFAFgIAAIjDAAQgpAAgTgZQgSgWAFglIA1kJQAHgmAbgaQATgSAagJIAOgEIC6guIAAgHIiOAAQgWAAgPgPQgQgQAAgWIAAmUQAAhxBRhRQBRhRBwAAQAmAAAqALQAqAKAfARQAFADAJgCQAQgDANAAQA1AAAqAsQApAqAFA4IABASQAAAIgFAFQgGAFgHAAQgEAAgFgCQgJgFAAgLIAAgPQgFgpgdghQgggjgoAAIgeAEQgQABgOgHQgcgQglgJQgmgJgiAAQhhAAhGBHQhGBGAABiIAAGUQAAAHAFAFQAFAFAHAAICOAAIAAgPQgdgPgXgWQgkgigUguQgUguAAgxIAAgqQAAgUAPgPQAPgOAVACIAVAAQBiAABPg0QAzgiAlgyQAKgOASABQARACAIAPQAPAgAgAEQAOACALAKQALAKADAOQASADAOAJIAAg0QAAgHAGgFQAFgGAIAAQAHAAAFAGQAGAFAAAHIAABjQADAQgDAPIAAENQAAAWgQAQQgQAPgWAAIiOAAIAAAHIC6AuIApARQAqAbAKAzIAvDqQAHAjAAALQAAAhgVASQgTASgiAAgAgqEfQATAWAXAAQAYAAATgWIAmgtIigAAgAhKCLQAAAGgEAFQgEAFgGACIg1ANIAfAkIDdAAIAfgkIg1gNQgJgDgEgJIgBgLIAAgyQhLAYhKgZgADwiSIAAAEQAABEgkA5QgiA3g7AeIAAAOICOAAQAHAAAFgFQAFgFAAgHIAAjeQgOAIgQADgAjGjDQgEADAAAJIAAAmQAAAqARAnQARAnAeAcQAuAsA9AKQA5AJA2gXQA3gXAhgvQAjgzAAhAIAAiOQAAgEgCgDQgDgDgEAAQgvgHgXgqQg5BJhOAmQhTAnhggFIgBAAQgDAAgEADgADwi3QAYgHAGgTIAAgVQgGgTgYgIg");
	this.shape.setTransform(44.4,61.5);
	this.timeline.addTween(cjs.Tween.get(this.shape).wait(1));
}).prototype = getMCSymbolPrototype(lib._4tdgdh, new cjs.Rectangle(0,0,88.8,123), null);
(lib._4srsdfdf = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f().ls(["#FC5D67","#F27D38"],[0,1],0,0.6,0,-0.3).ss(3,2,0,4).p("AAAnWIAAOs");
	this.shape.setTransform(0,47.1);
	this.timeline.addTween(cjs.Tween.get(this.shape).wait(1));
}).prototype = getMCSymbolPrototype(lib._4srsdfdf, new cjs.Rectangle(-1.5,-1.5,3,97.1), null);
(lib._4rtgfdfh = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f().ls(["#FC5D67","#F27D38"],[0,1],0,0.6,0,-0.4).ss(3,2,0,4).p("AAAnMIAAOY");
	this.shape.setTransform(0,46.1);
	this.timeline.addTween(cjs.Tween.get(this.shape).wait(1));
}).prototype = getMCSymbolPrototype(lib._4rtgfdfh, new cjs.Rectangle(-1.5,-1.5,3,95.1), null);
(lib._4etret = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f().ls(["#FA6062","#F27D38"],[0,1],0,24.1,0,-23.9).ss(3,0,0,4).p("AAAjvQBjAABGBHQBHBGAABiQAABjhHBHQhGBGhjAAQhiAAhHhGQhGhGAAhkQAAhiBGhGQBHhHBiAAg");
	this.shape.setTransform(24,24);
	this.shape_1 = new cjs.Shape();
	this.shape_1.graphics.f("#FFFFFF").s().p("AipCqQhGhGAAhkQAAhiBGhHQBHhGBiAAQBjAABGBGQBHBHAABiQAABjhHBHQhGBGhjAAQhiAAhHhGg");
	this.shape_1.setTransform(24,24);
	this.timeline.addTween(cjs.Tween.get({}).to({state:[{t:this.shape_1},{t:this.shape}]}).wait(1));
}).prototype = getMCSymbolPrototype(lib._4etret, new cjs.Rectangle(-1.5,-1.5,51,51), null);
(lib._4erert = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.shape = new cjs.Shape();
	this.shape.graphics.f("#FC5E67").s().p("AhUgiICpAAIhVBFg");
	this.shape.setTransform(8.5,3.5);
	this.timeline.addTween(cjs.Tween.get(this.shape).wait(1));
}).prototype = getMCSymbolPrototype(lib._4erert, new cjs.Rectangle(0,0,17,7), null);
(lib.trgrth = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.instance = new lib.GIFT();
	this.instance.parent = this;
	this.instance.setTransform(19.8,10.1,1,1,0,0,0,17.8,9.6);
	this.timeline.addTween(cjs.Tween.get(this.instance).wait(1));
}).prototype = getMCSymbolPrototype(lib.trgrth, new cjs.Rectangle(0,0,39.6,20), null);
(lib.tertet = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.instance = new lib.rgdgd();
	this.instance.parent = this;
	this.instance.setTransform(15.4,11.5,1,1,0,0,0,15.4,11.5);
	this.timeline.addTween(cjs.Tween.get(this.instance).wait(1));
}).prototype = getMCSymbolPrototype(lib.tertet, new cjs.Rectangle(0,0,30.8,23), null);
(lib.hfghfgh = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.instance = new lib.OGiExchange();
	this.instance.parent = this;
	this.instance.setTransform(67.5,12.1,1,1,0,0,0,65.5,12);
	this.timeline.addTween(cjs.Tween.get(this.instance).wait(1));
}).prototype = getMCSymbolPrototype(lib.hfghfgh, new cjs.Rectangle(-3,0,143.6,24), null);
(lib.he5eg = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.instance = new lib.Sponsor();
	this.instance.parent = this;
	this.instance.setTransform(40.8,12,1,1,0,0,0,38.8,12);
	this.timeline.addTween(cjs.Tween.get(this.instance).wait(1));
}).prototype = getMCSymbolPrototype(lib.he5eg, new cjs.Rectangle(0,0,81.7,24), null);
(lib.gfdgfdh = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.instance = new lib.Bob_0();
	this.instance.parent = this;
	this.instance.setTransform(21.1,12.1,1,1,0,0,0,19.1,12);
	this.timeline.addTween(cjs.Tween.get(this.instance).wait(1));
}).prototype = getMCSymbolPrototype(lib.gfdgfdh, new cjs.Rectangle(-1,1,50.2,24), null);
(lib.gfdgd = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.instance = new lib.John();
	this.instance.parent = this;
	this.instance.setTransform(24.9,12.1,1,1,0,0,0,22.9,12);
	this.timeline.addTween(cjs.Tween.get(this.instance).wait(1));
}).prototype = getMCSymbolPrototype(lib.gfdgd, new cjs.Rectangle(0,0,49.9,24), null);
(lib.erffgdfg = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.instance = new lib.Bob();
	this.instance.parent = this;
	this.instance.setTransform(21.1,12.1,1,1,0,0,0,19.1,12);
	this.timeline.addTween(cjs.Tween.get(this.instance).wait(1));
}).prototype = getMCSymbolPrototype(lib.erffgdfg, new cjs.Rectangle(0,0,42.3,24), null);
(lib._65пкупк = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 2
	this.instance = new lib.gre45();
	this.instance.parent = this;
	this.instance.setTransform(283.6,201.8,0.775,0.775,0,0,0,44.4,63.4);
	this.instance.alpha = 0;
	this.timeline.addTween(cjs.Tween.get(this.instance).to({scaleX:1.14,scaleY:1.14,x:283.7,y:201.9,alpha:1},12,cjs.Ease.get(-0.6)).to({regY:63.5,scaleX:0.96,scaleY:0.96,x:283.6,y:202},4).to({regY:63.4,scaleX:1,scaleY:1,y:201.8},3).wait(67));
	// $_1
	this.instance_1 = new lib._1();
	this.instance_1.parent = this;
	this.instance_1.setTransform(284.4,329.4,1,1,0,0,0,6.2,12);
	this.instance_1.alpha = 0;
	this.instance_1._off = true;
	this.timeline.addTween(cjs.Tween.get(this.instance_1).wait(50).to({_off:false},0).to({alpha:1},4).wait(32));
	// Layer 12
	this.instance_2 = new lib.rgrgfg();
	this.instance_2.parent = this;
	this.instance_2.setTransform(284.2,327.4,0.346,0.346,0,0,0,24,24);
	this.instance_2._off = true;
	this.timeline.addTween(cjs.Tween.get(this.instance_2).wait(50).to({_off:false},0).to({scaleX:1,scaleY:1},4).to({_off:true},1).wait(31));
	// Layer 11
	this.instance_3 = new lib.tryrty();
	this.instance_3.parent = this;
	this.instance_3.setTransform(284.2,327.4,0.346,0.346,0,0,0,24,24);
	this.instance_3._off = true;
	this.timeline.addTween(cjs.Tween.get(this.instance_3).wait(47).to({_off:false},0).to({scaleX:1,scaleY:1},3).to({_off:true},1).wait(35));
	// 4etret
	this.instance_4 = new lib._4etret();
	this.instance_4.parent = this;
	this.instance_4.setTransform(284.2,327.4,0.346,0.346,0,0,0,24,24);
	this.instance_4._off = true;
	this.timeline.addTween(cjs.Tween.get(this.instance_4).wait(47).to({_off:false},0).to({scaleX:1,scaleY:1},7).wait(32));
	// Layer 10 (mask)
	var mask = new cjs.Shape();
	mask._off = true;
	var mask_graphics_39 = new cjs.Graphics().p("AkzH5IAAvxIJnAAIAAPxg");
	this.timeline.addTween(cjs.Tween.get(mask).to({graphics:null,x:0,y:0}).wait(39).to({graphics:mask_graphics_39,x:284.4,y:327.5}).wait(47));
	// Layer 3
	this.instance_5 = new lib.teret();
	this.instance_5.parent = this;
	this.instance_5.setTransform(284.5,273,1,1,0,0,0,8.5,3.5);
	this.instance_5._off = true;
	var maskedShapeInstanceList = [this.instance_5];
	for(var shapedInstanceItr = 0; shapedInstanceItr < maskedShapeInstanceList.length; shapedInstanceItr++) {
		maskedShapeInstanceList[shapedInstanceItr].mask = mask;
	}
	this.timeline.addTween(cjs.Tween.get(this.instance_5).wait(39).to({_off:false},0).to({y:379},16).to({_off:true},1).wait(30));
	// fdgfdg
	this.instance_6 = new lib.fdgfdg();
	this.instance_6.parent = this;
	this.instance_6.setTransform(284.7,224,1,1,0,0,0,0,48.2);
	this.instance_6._off = true;
	var maskedShapeInstanceList = [this.instance_6];
	for(var shapedInstanceItr = 0; shapedInstanceItr < maskedShapeInstanceList.length; shapedInstanceItr++) {
		maskedShapeInstanceList[shapedInstanceItr].mask = mask;
	}
	this.timeline.addTween(cjs.Tween.get(this.instance_6).wait(39).to({_off:false},0).to({y:326},15).wait(32));
	// Layer 6
	this.instance_7 = new lib.Dоthetask();
	this.instance_7.parent = this;
	this.instance_7.setTransform(115.5,96.4,1,1,0,0,0,67.3,14.3);
	this.instance_7.alpha = 0;
	this.instance_7._off = true;
	this.timeline.addTween(cjs.Tween.get(this.instance_7).wait(27).to({_off:false},0).to({alpha:1},5).wait(54));
	// Layer 4
	this.instance_8 = new lib._45fdf();
	this.instance_8.parent = this;
	this.instance_8.setTransform(169.6,134.5,0.472,0.472,0,0,0,115.6,96.5);
	this.instance_8._off = true;
	this.timeline.addTween(cjs.Tween.get(this.instance_8).wait(22).to({_off:false},0).to({scaleX:1,scaleY:1,x:115.6,y:96.5},7).wait(57));
	// Layer 5
	this.instance_9 = new lib.he5eg();
	this.instance_9.parent = this;
	this.instance_9.setTransform(284,96.4,1,1,0,0,0,40.8,12);
	this.instance_9.alpha = 0;
	this.timeline.addTween(cjs.Tween.get(this.instance_9).to({y:116.4,alpha:1},12,cjs.Ease.get(0.66)).wait(74));
}).prototype = p = new cjs.MovieClip();
p.nominalBounds = new cjs.Rectangle(243.2,84.4,81.7,166.9);
(lib._45rsfdsf = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.instance = new lib._5ttrt();
	this.instance.parent = this;
	this.instance.setTransform(23.9,23.9,1,1,0,0,0,23.9,23.9);
	this.timeline.addTween(cjs.Tween.get(this.instance).wait(1));
}).prototype = getMCSymbolPrototype(lib._45rsfdsf, new cjs.Rectangle(-1.5,-1.5,51,51), null);
(lib._5thh = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.instance = new lib._0();
	this.instance.parent = this;
	this.instance.setTransform(8.2,12.1,1,1,0,0,0,6.2,12);
	this.timeline.addTween(cjs.Tween.get(this.instance).wait(1));
}).prototype = getMCSymbolPrototype(lib._5thh, new cjs.Rectangle(0,0,16.3,24), null);
(lib._5tet = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 2
	this.instance = new lib.rgdgd();
	this.instance.parent = this;
	this.instance.setTransform(14.6,12.1,1,1,0,0,0,15.4,11.5);
	this.timeline.addTween(cjs.Tween.get(this.instance).wait(1));
}).prototype = getMCSymbolPrototype(lib._5tet, new cjs.Rectangle(-0.8,0.6,30.8,23), null);
(lib._5ggf = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.instance = new lib._4rtgfdfh();
	this.instance.parent = this;
	this.instance.setTransform(0,46.1,1,1,0,0,0,0,46.1);
	this.timeline.addTween(cjs.Tween.get(this.instance).wait(1));
}).prototype = getMCSymbolPrototype(lib._5ggf, new cjs.Rectangle(-2,-2,4,96.1), null);
(lib._4ауаа = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 1
	this.instance = new lib.Fill1();
	this.instance.parent = this;
	this.instance.setTransform(35.8,28.1);
	this.instance_1 = new lib.GitHubProject();
	this.instance_1.parent = this;
	this.instance_1.setTransform(97.5,42.5,1,1,0,0,0,28.7,19.1);
	this.shape = new cjs.Shape();
	this.shape.graphics.f().s("#FFFFFF").ss(4,0,0,4).p("AJsnCIAAMJQAAAOALALQAKAKAOAAIBTAAIAAAqQAAAigYAXQgXAYgiAAI0hAAQgiAAgXgYQgYgYAAghIAAgqIBSAAQAOAAALgKQAKgLAAgOIAAsMQAAgNAJgJQAJgJANAAISWAAQANABAKAJQAKAKACAOgAqxnFIAALpIhTAAQgOAAgLAKQgKAKAAAPIAABNQAAA+AsAsQAtAsA+AAIUhAAQA+AAAsgsQAtgsAAg+IAAhNQAAgPgKgKQgKgKgPAAIhTAAIAArsQgEgqgegbQgegcgpAAIyWAAQgqAAgdAdQgdAeAAApg");
	this.shape.setTransform(80.8,55.4);
	this.shape_1 = new cjs.Shape();
	this.shape_1.graphics.lf(["#60BB97","#38C2CF"],[0,1],0,78.8,0,-78.7).s().p("AqQIqQg+AAgtgsQgsgsAAg+IAAhNQAAgPAKgKQALgKAOAAIBTAAIAArpQAAgpAdgeQAdgdAqAAISWAAQApAAAeAcQAeAbAEAqIAALsIBTAAQAPAAAKAKQAKAKAAAPIAABNQAAA+gtAsQgsAsg+AAgArhGUQAAAhAYAYQAXAYAiAAIUhAAQAiAAAXgYQAYgXAAgiIAAgqIhTAAQgOAAgKgKQgLgLAAgOIAAsJQgCgOgKgKQgKgJgNgBIyWAAQgNAAgJAJQgJAJAAANIAAMMQAAAOgKALQgLAKgOAAIhSAAg");
	this.shape_1.setTransform(80.8,55.4);
	this.shape_2 = new cjs.Shape();
	this.shape_2.graphics.f().s("#FFFFFF").ss(4,0,0,4).p("AiUALQAHAWASAMQARAOAVAAICqAAQAVAAASgOQARgMAIgWIEYAAQAOAAALgKQAKgKAAgOQAAgPgKgKQgLgKgOAAIk2AAQgPAAgKAKQgKAKAAAPIAAAHQAAAFgCABIijAAQgCgBAAgFIAAgHQAAgPgKgKQgKgKgPAAIk2AAQgOAAgLAKQgKAKAAAPQAAAOAKAKQAKAKAPAAg");
	this.shape_2.setTransform(80.8,88.1);
	this.shape_3 = new cjs.Shape();
	this.shape_3.graphics.f("#60BB98").s().p("AhVA7QgVAAgRgOQgSgNgHgVIkYAAQgPAAgKgKQgKgKAAgOQAAgOAKgLQALgKAOAAIE2AAQAPAAAKAKQAKALAAAOIAAAHQAAAFACABICjAAQACgBAAgFIAAgHQAAgOAKgLQAKgKAPAAIE2AAQAOAAALAKQAKALAAAOQAAAOgKAKQgLAKgOAAIkYAAQgIAVgRANQgSAOgVAAg");
	this.shape_3.setTransform(80.8,88.1);
	this.timeline.addTween(cjs.Tween.get({}).to({state:[{t:this.shape_3},{t:this.shape_2},{t:this.shape_1},{t:this.shape},{t:this.instance_1},{t:this.instance}]}).wait(1));
}).prototype = getMCSymbolPrototype(lib._4ауаа, new cjs.Rectangle(-2,-2,165.6,114.9), null);
(lib.s43sf = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// Layer 2
	this.instance = new lib._5tet();
	this.instance.parent = this;
	this.instance.setTransform(74,125.5,1,1,0,0,0,15.4,11.4);
	this.instance.alpha = 0;
	this.instance._off = true;
	this.timeline.addTween(cjs.Tween.get(this.instance).wait(13).to({_off:false},0).to({alpha:1},6).wait(141));
	// Layer 3
	this.instance_1 = new lib.rtret();
	this.instance_1.parent = this;
	this.instance_1.setTransform(73.4,125.7,0.424,0.424,0,0,0,23.7,23.9);
	this.instance_1._off = true;
	this.timeline.addTween(cjs.Tween.get(this.instance_1).wait(11).to({_off:false},0).to({regX:23.8,scaleX:1.11,scaleY:1.11,x:73.5},5).to({scaleX:1,scaleY:1,x:73.4},3).wait(141));
	// Layer 5
	this.instance_2 = new lib.eerfergg();
	this.instance_2.parent = this;
	this.instance_2.setTransform(-3.1,281.9,1,1,0,0,0,7.5,5.1);
	this.timeline.addTween(cjs.Tween.get(this.instance_2).to({x:133.9,y:7.2},19).wait(15).to({x:-3.1,y:281.1},0).to({x:133.9,y:7.2},30).wait(15).to({x:-3.1,y:281.1},0).to({x:133.9,y:7.2},30).wait(11).to({x:-3.1,y:281.1},0).to({x:133.9,y:7.2},30).wait(10));
	// Layer 10 (mask)
	var mask = new cjs.Shape();
	mask._off = true;
	mask.graphics.p("A3yN+MAWzgphIYyNlMgWzApjg");
	mask.setTransform(53.8,134.2);
	// Layer 4
	this.instance_3 = new lib.terert();
	this.instance_3.parent = this;
	this.instance_3.setTransform(-69.6,416.2,1,1,0,0,0,67.4,134.5);
	var maskedShapeInstanceList = [this.instance_3];
	for(var shapedInstanceItr = 0; shapedInstanceItr < maskedShapeInstanceList.length; shapedInstanceItr++) {
		maskedShapeInstanceList[shapedInstanceItr].mask = mask;
	}
	this.timeline.addTween(cjs.Tween.get(this.instance_3).to({x:67.4,y:141.5},19).wait(141));
	// Layer 6
	this.instance_4 = new lib.tertet();
	this.instance_4.parent = this;
	this.instance_4.setTransform(269.5,126.9,1,1,0,0,0,15.4,11.5);
	this.instance_4.alpha = 0;
	this.instance_4._off = true;
	this.timeline.addTween(cjs.Tween.get(this.instance_4).wait(13).to({_off:false},0).to({alpha:1},6).wait(141));
	// Layer 7
	this.instance_5 = new lib.tertre();
	this.instance_5.parent = this;
	this.instance_5.setTransform(269.5,126.3,0.417,0.417,0,0,0,24,24);
	this.instance_5._off = true;
	this.timeline.addTween(cjs.Tween.get(this.instance_5).wait(11).to({_off:false},0).to({scaleX:1.13,scaleY:1.13},5).to({scaleX:1,scaleY:1},3).wait(141));
	// Layer 9
	this.instance_6 = new lib._5ttrtrere();
	this.instance_6.parent = this;
	this.instance_6.setTransform(345,281.7,1,1,0,0,0,7.8,4.9);
	this.timeline.addTween(cjs.Tween.get(this.instance_6).to({x:213.9,y:4.9},19).wait(15).to({x:343,y:276},0).to({x:213.9,y:4.9},30).wait(15).to({x:343,y:276},0).to({x:213.9,y:4.9},30).wait(11).to({x:343,y:276},0).to({x:213.9,y:4.9},30).wait(10));
	// Layer 11 (mask)
	var mask_1 = new cjs.Shape();
	mask_1._off = true;
	mask_1.graphics.p("Atgt9IYytmMAWyAphI4zNmg");
	mask_1.setTransform(218,137.2);
	// Layer 8
	this.instance_7 = new lib._5etrt();
	this.instance_7.parent = this;
	this.instance_7.setTransform(409.1,417.6,1,1,0,0,0,64.5,136);
	var maskedShapeInstanceList = [this.instance_7];
	for(var shapedInstanceItr = 0; shapedInstanceItr < maskedShapeInstanceList.length; shapedInstanceItr++) {
		maskedShapeInstanceList[shapedInstanceItr].mask = mask_1;
	}
	this.timeline.addTween(cjs.Tween.get(this.instance_7).to({x:278.1,y:140.8},19).wait(141));
}).prototype = p = new cjs.MovieClip();
p.nominalBounds = new cjs.Rectangle(-98.4,276.8,534.5,36.8);
(lib.dsfsf = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// OGi-Exchange
	this.instance = new lib.hfghfgh();
	this.instance.parent = this;
	this.instance.setTransform(78.5,320,1,1,0,0,0,67.5,12);
	this.instance.alpha = 0;
	this.instance._off = true;
	this.timeline.addTween(cjs.Tween.get(this.instance).wait(9).to({_off:false},0).to({alpha:1},19).wait(105));
	// Layer 3
	this.instance_1 = new lib.tythhfh();
	this.instance_1.parent = this;
	this.instance_1.setTransform(76,208.2,1.612,1.612,0,0,0,14.5,26.3);
	this.instance_1._off = true;
	this.timeline.addTween(cjs.Tween.get(this.instance_1).wait(17).to({_off:false},0).to({regX:14.6,scaleX:0.89,scaleY:0.89,x:76.2,y:208.1},5).to({regX:14.5,regY:26.2,scaleX:1,scaleY:1,x:76,y:208},6).wait(105));
	// Layer 10
	this.instance_2 = new lib.hgfhhj();
	this.instance_2.parent = this;
	this.instance_2.setTransform(76,184.2,0.442,0.442,0,0,0,14.2,22.3);
	this.instance_2.alpha = 0;
	this.instance_2._off = true;
	this.timeline.addTween(cjs.Tween.get(this.instance_2).wait(9).to({_off:false},0).to({regX:14.1,regY:22.2,scaleX:1.13,scaleY:1.13,x:75.9,y:147.1,alpha:1},13,cjs.Ease.get(0.52)).to({regX:14,scaleX:1,scaleY:1,y:154.2},6).to({_off:true},4).wait(2).to({_off:false},0).wait(99));
	// Layer 5
	this.instance_3 = new lib.rhh();
	this.instance_3.parent = this;
	this.instance_3.setTransform(93.5,190.4,0.442,0.442,0,0,0,18.4,18.2);
	this.instance_3.alpha = 0;
	this.instance_3._off = true;
	this.timeline.addTween(cjs.Tween.get(this.instance_3).wait(9).to({_off:false},0).to({regX:18.2,regY:18.3,scaleX:1.13,scaleY:1.13,x:120.6,y:163.2,alpha:1},13,cjs.Ease.get(0.52)).to({regY:18.2,scaleX:1,scaleY:1,x:115.4,y:168.3},6).to({_off:true},7).wait(2).to({_off:false},0).wait(96));
	// Layer 9
	this.instance_4 = new lib.trhrth();
	this.instance_4.parent = this;
	this.instance_4.setTransform(99.7,208,0.442,0.442,0,0,0,22.2,14.1);
	this.instance_4.alpha = 0;
	this.instance_4._off = true;
	this.timeline.addTween(cjs.Tween.get(this.instance_4).wait(9).to({_off:false},0).to({scaleX:1.13,scaleY:1.13,x:136.6,alpha:1},13,cjs.Ease.get(0.52)).to({regY:14,scaleX:1,scaleY:1,x:129.6,y:207.9},6).to({_off:true},10).wait(2).to({_off:false},0).wait(93));
	// Layer 7
	this.instance_5 = new lib.hhfhfh();
	this.instance_5.parent = this;
	this.instance_5.setTransform(93.5,225.4,0.442,0.442,0,0,0,18.4,18.2);
	this.instance_5.alpha = 0;
	this.instance_5._off = true;
	this.timeline.addTween(cjs.Tween.get(this.instance_5).wait(9).to({_off:false},0).to({regX:18.2,scaleX:1.13,scaleY:1.13,x:120.7,y:252.7,alpha:1},13,cjs.Ease.get(0.52)).to({scaleX:1,scaleY:1,x:115.5,y:247.5},6).to({_off:true},13).wait(2).to({_off:false},0).wait(90));
	// Layer 11
	this.instance_6 = new lib.thgfh();
	this.instance_6.parent = this;
	this.instance_6.setTransform(76,231.7,0.442,0.442,0,0,0,14.2,22.3);
	this.instance_6.alpha = 0;
	this.instance_6._off = true;
	this.timeline.addTween(cjs.Tween.get(this.instance_6).wait(9).to({_off:false},0).to({regX:14.1,regY:22.2,scaleX:1.13,scaleY:1.13,x:75.9,y:268.6,alpha:1},13,cjs.Ease.get(0.52)).to({regX:14,scaleX:1,scaleY:1,y:261.6},6).to({_off:true},16).wait(2).to({_off:false},0).wait(87));
	// Layer 4
	this.instance_7 = new lib._5tgh();
	this.instance_7.parent = this;
	this.instance_7.setTransform(58.5,225.4,0.442,0.442,0,0,0,18.2,18.2);
	this.instance_7.alpha = 0;
	this.instance_7._off = true;
	this.timeline.addTween(cjs.Tween.get(this.instance_7).wait(9).to({_off:false},0).to({regX:18.3,scaleX:1.13,scaleY:1.13,x:31.2,y:252.7,alpha:1},13,cjs.Ease.get(0.52)).to({regX:18.2,scaleX:1,scaleY:1,x:36.3,y:247.5},6).to({_off:true},19).wait(2).to({_off:false},0).wait(84));
	// Layer 8
	this.instance_8 = new lib.trhtrh();
	this.instance_8.parent = this;
	this.instance_8.setTransform(52.3,208,0.442,0.442,0,0,0,22.3,14.1);
	this.instance_8.alpha = 0;
	this.instance_8._off = true;
	this.timeline.addTween(cjs.Tween.get(this.instance_8).wait(9).to({_off:false},0).to({regX:22.2,scaleX:1.13,scaleY:1.13,x:15.1,alpha:1},13,cjs.Ease.get(0.52)).to({regY:14,scaleX:1,scaleY:1,x:22.2,y:207.9},6).to({_off:true},22).wait(2).to({_off:false},0).wait(81));
	// Layer 6
	this.instance_9 = new lib.trhgfhhj();
	this.instance_9.parent = this;
	this.instance_9.setTransform(58.5,190.4,0.442,0.442,0,0,0,18.2,18.2);
	this.instance_9.alpha = 0;
	this.instance_9._off = true;
	this.timeline.addTween(cjs.Tween.get(this.instance_9).wait(9).to({_off:false},0).to({regX:18.3,regY:18.3,scaleX:1.13,scaleY:1.13,x:31.2,y:163.2,alpha:1},13,cjs.Ease.get(0.52)).to({regX:18.2,regY:18.2,scaleX:1,scaleY:1,x:36.3,y:168.3},6).to({_off:true},25).wait(2).to({_off:false},0).wait(78));
	// $_0
	this.instance_10 = new lib._5thh();
	this.instance_10.parent = this;
	this.instance_10.setTransform(111.2,57,1,1,0,0,0,8.2,12);
	this.instance_10.alpha = 0;
	this.instance_10._off = true;
	this.timeline.addTween(cjs.Tween.get(this.instance_10).wait(76).to({_off:false},0).to({alpha:1},3).wait(54));
	// Layer 18
	this.instance_11 = new lib._566hrhf();
	this.instance_11.parent = this;
	this.instance_11.setTransform(111.1,55.1,0.521,0.521,0,0,0,24,24);
	this.instance_11._off = true;
	this.timeline.addTween(cjs.Tween.get(this.instance_11).wait(70).to({_off:false},0).to({scaleX:1,scaleY:1,x:111,y:55},7).wait(56));
	// Layer 12
	this.instance_12 = new lib._45tgfbgfb();
	this.instance_12.parent = this;
	this.instance_12.setTransform(110.3,105.5,1,1,0,0,0,8.5,3.5);
	this.instance_12._off = true;
	this.timeline.addTween(cjs.Tween.get(this.instance_12).wait(62).to({_off:false},0).to({x:110.5,y:3.5},15).wait(56));
	// Layer 21 (mask)
	var mask = new cjs.Shape();
	mask._off = true;
	var mask_graphics_62 = new cjs.Graphics().p("Ah8IDIAAwFID5AAIAAQFg");
	this.timeline.addTween(cjs.Tween.get(mask).to({graphics:null,x:0,y:0}).wait(62).to({graphics:mask_graphics_62,x:113,y:51.5}).wait(71));
	// Layer 19
	this.instance_13 = new lib._5trgrh();
	this.instance_13.parent = this;
	this.instance_13.setTransform(110.3,156.5,1,1,0,0,0,0,47.1);
	this.instance_13._off = true;
	var maskedShapeInstanceList = [this.instance_13];
	for(var shapedInstanceItr = 0; shapedInstanceItr < maskedShapeInstanceList.length; shapedInstanceItr++) {
		maskedShapeInstanceList[shapedInstanceItr].mask = mask;
	}
	this.timeline.addTween(cjs.Tween.get(this.instance_13).wait(62).to({_off:false},0).to({x:110.5,y:54.5},15).wait(56));
	// GIFT
	this.instance_14 = new lib.trgrth();
	this.instance_14.parent = this;
	this.instance_14.setTransform(42.3,57,1,1,0,0,0,19.8,10);
	this.instance_14.alpha = 0;
	this.instance_14._off = true;
	this.timeline.addTween(cjs.Tween.get(this.instance_14).wait(13).to({_off:false},0).to({alpha:1},3).wait(117));
	// Layer 15
	this.instance_15 = new lib._5ggfg();
	this.instance_15.parent = this;
	this.instance_15.setTransform(42,55,0.479,0.479,0,0,0,24,24);
	this.instance_15._off = true;
	this.timeline.addTween(cjs.Tween.get(this.instance_15).wait(7).to({_off:false},0).to({scaleX:1,scaleY:1},7).wait(119));
	// Layer 13
	this.instance_16 = new lib.ggrrth();
	this.instance_16.parent = this;
	this.instance_16.setTransform(41,3.9,1,1,0,0,0,8.5,3.5);
	this.timeline.addTween(cjs.Tween.get(this.instance_16).to({x:41.5,y:102.5},14).wait(119));
	// Layer 20 (mask)
	var mask_1 = new cjs.Shape();
	mask_1._off = true;
	mask_1.graphics.p("Aj7H3IAAvtIH4AAIAAPtg");
	mask_1.setTransform(38.2,55.8);
	// Layer 16
	this.instance_17 = new lib._4srsdfdf();
	this.instance_17.parent = this;
	this.instance_17.setTransform(41,-44.2,1,1,0,0,0,0,47.1);
	var maskedShapeInstanceList = [this.instance_17];
	for(var shapedInstanceItr = 0; shapedInstanceItr < maskedShapeInstanceList.length; shapedInstanceItr++) {
		maskedShapeInstanceList[shapedInstanceItr].mask = mask_1;
	}
	this.timeline.addTween(cjs.Tween.get(this.instance_17).to({x:41.5,y:54.5},14).wait(119));
}).prototype = p = new cjs.MovieClip();
p.nominalBounds = new cjs.Rectangle(32.5,0.4,17,7);
(lib._45авап = function(mode,startPosition,loop) {
	this.initialize(mode,startPosition,loop,{});
	// GIFT_2
	this.instance = new lib.GIFT_2();
	this.instance.parent = this;
	this.instance.setTransform(393.4,256.8,1,1,0,0,0,17.8,9.6);
	this.instance.alpha = 0;
	this.instance._off = true;
	this.timeline.addTween(cjs.Tween.get(this.instance).wait(127).to({_off:false},0).to({alpha:1},4).wait(19));
	// Layer 3
	this.instance_1 = new lib.eetert();
	this.instance_1.parent = this;
	this.instance_1.setTransform(393.2,254.9,1.383,1.383,0,0,0,24.1,24);
	this.instance_1._off = true;
	this.timeline.addTween(cjs.Tween.get(this.instance_1).wait(122).to({_off:false},0).to({scaleX:0.84,scaleY:0.84,x:393.1,y:254.8},5).to({regX:24,regY:23.9,scaleX:1,scaleY:1,x:393,y:254.7},4).wait(19));
	// GIFT_0
	this.instance_2 = new lib.GIFT_0();
	this.instance_2.parent = this;
	this.instance_2.setTransform(283.8,269.6,1,1,0,0,0,17.8,9.6);
	this.instance_2.alpha = 0;
	this.instance_2._off = true;
	this.timeline.addTween(cjs.Tween.get(this.instance_2).wait(118).to({_off:false},0).to({alpha:1},4).wait(28));
	// 4terdhh
	this.instance_3 = new lib._4terdhh();
	this.instance_3.parent = this;
	this.instance_3.setTransform(284.1,267.7,1.419,1.419,0,0,0,24,24);
	this.instance_3._off = true;
	this.timeline.addTween(cjs.Tween.get(this.instance_3).wait(112).to({_off:false},0).to({scaleX:0.82,scaleY:0.82},6).to({scaleX:1,scaleY:1,x:284,y:267.6},4).wait(28));
	// Layer 45
	this.instance_4 = new lib.GIFT_1();
	this.instance_4.parent = this;
	this.instance_4.setTransform(183.5,258.8,1,1,0,0,0,17.8,9.6);
	this.instance_4.alpha = 0;
	this.instance_4._off = true;
	this.timeline.addTween(cjs.Tween.get(this.instance_4).wait(112).to({_off:false},0).to({alpha:1},4).wait(34));
	// Layer 8
	this.instance_5 = new lib._45rsfdsf();
	this.instance_5.parent = this;
	this.instance_5.setTransform(184.3,257.6,1.39,1.39,0,0,0,24,24);
	this.instance_5._off = true;
	this.timeline.addTween(cjs.Tween.get(this.instance_5).wait(106).to({_off:false},0).to({regX:24.1,regY:24.1,scaleX:0.91,scaleY:0.91,x:184.4,y:257.7},6).to({regX:23.9,regY:23.9,scaleX:1,scaleY:1,x:184.2,y:257.5},4).wait(34));
	// Layer 4
	this.instance_6 = new lib.gfdgd();
	this.instance_6.parent = this;
	this.instance_6.setTransform(500.9,245.6,1,1,0,0,0,24.9,12);
	this.instance_6.alpha = 0;
	this.instance_6._off = true;
	this.timeline.addTween(cjs.Tween.get(this.instance_6).wait(52).to({_off:false},0).to({alpha:1},6).wait(92));
	// Layer 6
	this.instance_7 = new lib.rgfdhh();
	this.instance_7.parent = this;
	this.instance_7.setTransform(502.5,331.2,0.528,0.528,0,0,0,44.3,61.6);
	this.instance_7.alpha = 0;
	this.instance_7._off = true;
	this.timeline.addTween(cjs.Tween.get(this.instance_7).wait(41).to({_off:false},0).to({regX:44.4,scaleX:1.07,scaleY:1.07,x:502.6,alpha:1},11).to({scaleX:0.93,scaleY:0.93,x:502.5,y:331.3},3).to({regY:61.5,scaleX:1,scaleY:1,y:331.1},3).wait(92));
	// Layer 51 (mask)
	var mask = new cjs.Shape();
	mask._off = true;
	var mask_graphics_41 = new cjs.Graphics().p("AqAhtIIEoQIL9LrIoFIQg");
	this.timeline.addTween(cjs.Tween.get(mask).to({graphics:null,x:0,y:0}).wait(41).to({graphics:mask_graphics_41,x:394,y:259.7}).wait(109));
	// Layer 44
	this.instance_8 = new lib.tergrgrg();
	this.instance_8.parent = this;
	this.instance_8.setTransform(353.8,214,1,1,0,0,0,6,6);
	this.instance_8._off = true;
	var maskedShapeInstanceList = [this.instance_8];
	for(var shapedInstanceItr = 0; shapedInstanceItr < maskedShapeInstanceList.length; shapedInstanceItr++) {
		maskedShapeInstanceList[shapedInstanceItr].mask = mask;
	}
	this.timeline.addTween(cjs.Tween.get(this.instance_8).wait(41).to({_off:false},0).to({x:427,y:287.6},11).wait(98));
	// Layer 43
	this.instance_9 = new lib.tergg();
	this.instance_9.parent = this;
	this.instance_9.setTransform(319.8,180.4,1,1,0,0,0,33.3,33.2);
	this.instance_9._off = true;
	var maskedShapeInstanceList = [this.instance_9];
	for(var shapedInstanceItr = 0; shapedInstanceItr < maskedShapeInstanceList.length; shapedInstanceItr++) {
		maskedShapeInstanceList[shapedInstanceItr].mask = mask;
	}
	this.timeline.addTween(cjs.Tween.get(this.instance_9).wait(41).to({_off:false},0).to({x:393,y:254},11).wait(98));
	// Layer 42
	this.instance_10 = new lib.gfdgfdh();
	this.instance_10.parent = this;
	this.instance_10.setTransform(280.1,346.6,1,1,0,0,0,21.1,12);
	this.instance_10.alpha = 0;
	this.instance_10._off = true;
	this.timeline.addTween(cjs.Tween.get(this.instance_10).wait(41).to({_off:false},0).to({alpha:1},6).wait(103));
	// Layer 41
	this.instance_11 = new lib._4tdgdh();
	this.instance_11.parent = this;
	this.instance_11.setTransform(283.5,429.1,0.598,0.598,0,0,0,44.3,61.5);
	this.instance_11.alpha = 0;
	this.instance_11._off = true;
	this.timeline.addTween(cjs.Tween.get(this.instance_11).wait(31).to({_off:false},0).to({regX:44.5,scaleX:1.05,scaleY:1.05,x:283.7,y:429.2,alpha:1},10).to({regX:44.4,scaleX:0.91,scaleY:0.91,x:283.5,y:429.1},3).to({scaleX:1,scaleY:1},3).wait(103));
	// Layer 50 (mask)
	var mask_1 = new cjs.Shape();
	mask_1._off = true;
	var mask_1_graphics_31 = new cjs.Graphics().p("AlOIcIAAw3IKdAAIAAQ3g");
	this.timeline.addTween(cjs.Tween.get(mask_1).to({graphics:null,x:0,y:0}).wait(31).to({graphics:mask_1_graphics_31,x:283.5,y:273.2}).wait(119));
	// Layer 40
	this.instance_12 = new lib._4erert();
	this.instance_12.parent = this;
	this.instance_12.setTransform(283.5,217.6,1,1,0,0,0,8.5,3.5);
	this.instance_12._off = true;
	var maskedShapeInstanceList = [this.instance_12];
	for(var shapedInstanceItr = 0; shapedInstanceItr < maskedShapeInstanceList.length; shapedInstanceItr++) {
		maskedShapeInstanceList[shapedInstanceItr].mask = mask_1;
	}
	this.timeline.addTween(cjs.Tween.get(this.instance_12).wait(31).to({_off:false},0).to({y:315.1},10).wait(109));
	// Layer 7
	this.instance_13 = new lib._7resgfd();
	this.instance_13.parent = this;
	this.instance_13.setTransform(283.5,169.5,1,1,0,0,0,0,47);
	this.instance_13._off = true;
	var maskedShapeInstanceList = [this.instance_13];
	for(var shapedInstanceItr = 0; shapedInstanceItr < maskedShapeInstanceList.length; shapedInstanceItr++) {
		maskedShapeInstanceList[shapedInstanceItr].mask = mask_1;
	}
	this.timeline.addTween(cjs.Tween.get(this.instance_13).wait(31).to({_off:false},0).to({y:267},10).wait(109));
	// Layer 39
	this.instance_14 = new lib.erffgdfg();
	this.instance_14.parent = this;
	this.instance_14.setTransform(70.1,242.6,1,1,0,0,0,21.1,12);
	this.instance_14.alpha = 0;
	this.instance_14._off = true;
	this.timeline.addTween(cjs.Tween.get(this.instance_14).wait(31).to({_off:false},0).to({alpha:1},6).wait(113));
	// Layer 38
	this.instance_15 = new lib.refgfdgfd();
	this.instance_15.parent = this;
	this.instance_15.setTransform(70.6,327.1,0.369,0.369,0,0,0,44.4,61.5);
	this.instance_15.alpha = 0;
	this.instance_15._off = true;
	this.timeline.addTween(cjs.Tween.get(this.instance_15).wait(21).to({_off:false},0).to({regX:44.5,scaleX:1.14,scaleY:1.14,x:70.7,alpha:1},10).to({regY:61.6,scaleX:0.95,scaleY:0.95,y:327.2},3).to({regX:44.4,regY:61.5,scaleX:1,scaleY:1,x:70.6,y:327.1},3).wait(113));
	// Layer 49 (mask)
	var mask_2 = new cjs.Shape();
	mask_2._off = true;
	var mask_2_graphics_21 = new cjs.Graphics().p("AglRtILWsMIIgHxIrXMMg");
	this.timeline.addTween(cjs.Tween.get(mask_2).to({graphics:null,x:0,y:0}).wait(21).to({graphics:mask_2_graphics_21,x:123.3,y:163}).wait(129));
	// Layer 9
	this.instance_16 = new lib.teggfg();
	this.instance_16.parent = this;
	this.instance_16.setTransform(222.5,218.1,1,1,0,0,0,6,6);
	this.instance_16._off = true;
	var maskedShapeInstanceList = [this.instance_16];
	for(var shapedInstanceItr = 0; shapedInstanceItr < maskedShapeInstanceList.length; shapedInstanceItr++) {
		maskedShapeInstanceList[shapedInstanceItr].mask = mask_2;
	}
	this.timeline.addTween(cjs.Tween.get(this.instance_16).wait(21).to({_off:false},0).to({x:151,y:289.6},10).wait(119));
	// Layer 37
	this.instance_17 = new lib.rwefe();
	this.instance_17.parent = this;
	this.instance_17.setTransform(255.8,185.3,1,1,0,0,0,33.3,33.3);
	this.instance_17._off = true;
	var maskedShapeInstanceList = [this.instance_17];
	for(var shapedInstanceItr = 0; shapedInstanceItr < maskedShapeInstanceList.length; shapedInstanceItr++) {
		maskedShapeInstanceList[shapedInstanceItr].mask = mask_2;
	}
	this.timeline.addTween(cjs.Tween.get(this.instance_17).wait(21).to({_off:false},0).to({x:184.3,y:256.8},10).wait(119));
	// 50%
	this.instance_18 = new lib._50();
	this.instance_18.parent = this;
	this.instance_18.setTransform(512.1,429.1,1,1,0,0,0,20.1,10.8);
	this.instance_18.alpha = 0;
	this.instance_18._off = true;
	this.timeline.addTween(cjs.Tween.get(this.instance_18).wait(87).to({_off:false},0).to({alpha:1},3).wait(60));
	// Layer 48 (mask)
	var mask_3 = new cjs.Shape();
	mask_3._off = true;
	var mask_3_graphics_74 = new cjs.Graphics().p("EAWvAgeQgVAAgPgOQgOgPAAgVQAAgVAOgOQAPgPAVAAIWCAAQAVAAAPAPQAOAOAAAVQAAAVgOAPQgPAOgVAAg");
	this.timeline.addTween(cjs.Tween.get(mask_3).to({graphics:null,x:0,y:0}).wait(74).to({graphics:mask_3_graphics_74,x:291.5,y:207.8}).wait(76));
	// Layer 12
	this.instance_19 = new lib.thrhrhgh();
	this.instance_19.parent = this;
	this.instance_19.setTransform(392,410.6,1,1,0,0,0,40,5);
	this.instance_19._off = true;
	var maskedShapeInstanceList = [this.instance_19];
	for(var shapedInstanceItr = 0; shapedInstanceItr < maskedShapeInstanceList.length; shapedInstanceItr++) {
		maskedShapeInstanceList[shapedInstanceItr].mask = mask_3;
	}
	this.timeline.addTween(cjs.Tween.get(this.instance_19).wait(74).to({_off:false},0).to({x:472},13).wait(63));
	// Layer 13
	this.instance_20 = new lib._5tergrt();
	this.instance_20.parent = this;
	this.instance_20.setTransform(507.5,410.6,1,1,0,0,0,75.5,5);
	this.instance_20.alpha = 0;
	this.instance_20._off = true;
	this.timeline.addTween(cjs.Tween.get(this.instance_20).wait(72).to({_off:false},0).to({alpha:1},2).wait(76));
	// 30%
	this.instance_21 = new lib._30();
	this.instance_21.parent = this;
	this.instance_21.setTransform(285.1,530.1,1,1,0,0,0,20.1,10.8);
	this.instance_21.alpha = 0;
	this.instance_21._off = true;
	this.timeline.addTween(cjs.Tween.get(this.instance_21).wait(82).to({_off:false},0).to({alpha:1},3).wait(65));
	// Layer 47 (mask)
	var mask_4 = new cjs.Shape();
	mask_4._off = true;
	var mask_4_graphics_71 = new cjs.Graphics().p("EAFZAoXQgUAAgQgOQgOgPAAgVQAAgVAOgPQAQgOAUAAIWCAAQAUAAAPAOQAPAPAAAVQAAAVgPAPQgPAOgUAAg");
	this.timeline.addTween(cjs.Tween.get(mask_4).to({graphics:null,x:0,y:0}).wait(71).to({graphics:mask_4_graphics_71,x:180.5,y:258.3}).wait(79));
	// Layer 34
	this.instance_22 = new lib.yrtyrtytry();
	this.instance_22.parent = this;
	this.instance_22.setTransform(172.3,511.6,1,1,0,0,0,35.3,5);
	this.instance_22._off = true;
	var maskedShapeInstanceList = [this.instance_22];
	for(var shapedInstanceItr = 0; shapedInstanceItr < maskedShapeInstanceList.length; shapedInstanceItr++) {
		maskedShapeInstanceList[shapedInstanceItr].mask = mask_4;
	}
	this.timeline.addTween(cjs.Tween.get(this.instance_22).wait(71).to({_off:false},0).to({x:245.3},11).wait(68));
	// Layer 35
	this.instance_23 = new lib.ergg();
	this.instance_23.parent = this;
	this.instance_23.setTransform(285.5,511.6,1,1,0,0,0,75.5,5);
	this.instance_23.alpha = 0;
	this.instance_23._off = true;
	this.timeline.addTween(cjs.Tween.get(this.instance_23).wait(69).to({_off:false},0).to({alpha:1},2).wait(79));
	// 20%
	this.instance_24 = new lib._20();
	this.instance_24.parent = this;
	this.instance_24.setTransform(56.1,426.1,1,1,0,0,0,20.1,10.8);
	this.instance_24.alpha = 0;
	this.instance_24._off = true;
	this.timeline.addTween(cjs.Tween.get(this.instance_24).wait(78).to({_off:false},0).to({alpha:1},3).wait(69));
	// Layer 46 (mask)
	var mask_5 = new cjs.Shape();
	mask_5._off = true;
	var mask_5_graphics_66 = new cjs.Graphics().p("EgLAAgPQgVAAgPgPQgOgPAAgUQAAgVAOgPQAPgOAVAAIWBAAQAVAAAPAOQAOAPAAAVQAAAUgOAPQgPAPgVAAg");
	this.timeline.addTween(cjs.Tween.get(mask_5).to({graphics:null,x:0,y:0}).wait(66).to({graphics:mask_5_graphics_66,x:75.5,y:206.3}).wait(84));
	// Layer 29
	this.instance_25 = new lib.rtgrtf();
	this.instance_25.parent = this;
	this.instance_25.setTransform(-26,407.6,1,1,0,0,0,26,5);
	this.instance_25._off = true;
	var maskedShapeInstanceList = [this.instance_25];
	for(var shapedInstanceItr = 0; shapedInstanceItr < maskedShapeInstanceList.length; shapedInstanceItr++) {
		maskedShapeInstanceList[shapedInstanceItr].mask = mask_5;
	}
	this.timeline.addTween(cjs.Tween.get(this.instance_25).wait(68).to({_off:false},0).to({x:26},10).wait(72));
	// Layer 30
	this.instance_26 = new lib.f5g();
	this.instance_26.parent = this;
	this.instance_26.setTransform(75.5,407.6,1,1,0,0,0,75.5,5);
	this.instance_26.alpha = 0;
	this.instance_26._off = true;
	this.timeline.addTween(cjs.Tween.get(this.instance_26).wait(66).to({_off:false},0).to({alpha:1},2).wait(82));
	// OGi-Cloud
	this.instance_27 = new lib.OGiCloud();
	this.instance_27.parent = this;
	this.instance_27.setTransform(286.3,167.6,1,1,0,0,0,47.3,12);
	this.instance_27.alpha = 0;
	this.timeline.addTween(cjs.Tween.get(this.instance_27).to({alpha:1},9).wait(141));
	// Layer 20
	this.instance_28 = new lib._5ttrrh();
	this.instance_28.parent = this;
	this.instance_28.setTransform(287.2,154.4,0.74,0.74,0,0,0,81,56.8);
	this.instance_28.alpha = 0;
	this.timeline.addTween(cjs.Tween.get(this.instance_28).to({regY:56.6,scaleX:1.06,scaleY:1.06,y:154.2,alpha:1},9).to({regX:80.9,scaleX:1,scaleY:1,x:287.1},3).wait(138));
	// $
	this.instance_29 = new lib.Symbol();
	this.instance_29.parent = this;
	this.instance_29.setTransform(286.7,48.6,1,1,0,0,0,6.2,12);
	this.instance_29.alpha = 0;
	this.instance_29._off = true;
	this.timeline.addTween(cjs.Tween.get(this.instance_29).wait(8).to({_off:false},0).to({alpha:1},4).wait(138));
	// e45tdg
	this.instance_30 = new lib.e45tdg();
	this.instance_30.parent = this;
	this.instance_30.setTransform(286.1,46.7,0.579,0.579,0,0,0,24.1,24.1);
	this.instance_30._off = true;
	this.timeline.addTween(cjs.Tween.get(this.instance_30).wait(6).to({_off:false},0).to({regX:24,regY:24,scaleX:1,scaleY:1,x:286,y:46.6},6).wait(138));
	// Layer 24 (mask)
	var mask_6 = new cjs.Shape();
	mask_6._off = true;
	mask_6.graphics.p("AkmHbIAAu1IJNAAIAAO1g");
	mask_6.setTransform(284.5,46.2);
	// Layer 18
	this.instance_31 = new lib._56hgfhg();
	this.instance_31.parent = this;
	this.instance_31.setTransform(286.5,-5.2,1,1,0,0,0,8.5,3.5);
	var maskedShapeInstanceList = [this.instance_31];
	for(var shapedInstanceItr = 0; shapedInstanceItr < maskedShapeInstanceList.length; shapedInstanceItr++) {
		maskedShapeInstanceList[shapedInstanceItr].mask = mask_6;
	}
	this.timeline.addTween(cjs.Tween.get(this.instance_31).to({y:91.8},12).wait(1).to({y:93.8},0).wait(1).to({y:95.8},0).to({_off:true},1).wait(135));
	// 4rtgfdfh
	this.instance_32 = new lib._5ggf();
	this.instance_32.parent = this;
	this.instance_32.setTransform(286.5,-50.9,1,1,0,0,0,0,46.1);
	var maskedShapeInstanceList = [this.instance_32];
	for(var shapedInstanceItr = 0; shapedInstanceItr < maskedShapeInstanceList.length; shapedInstanceItr++) {
		maskedShapeInstanceList[shapedInstanceItr].mask = mask_6;
	}
	this.timeline.addTween(cjs.Tween.get(this.instance_32).to({y:46.1},12).wait(138));
}).prototype = p = new cjs.MovieClip();
p.nominalBounds = new cjs.Rectangle(225.4,110.5,123.5,87.6);
// stage content:
(lib.index = function(mode,startPosition,loop) {
if (loop == null) { loop = false; }	this.initialize(mode,startPosition,loop,{clip1:9,clip2:79,clip3:229,clip4:380});
	// Layer 5
	this.instance = new lib.dsfsf("synched",0,false);
	this.instance.parent = this;
	this.instance.setTransform(285.9,1235.4,1,1,0,0,0,75.9,166);
	this.instance._off = true;
	this.timeline.addTween(cjs.Tween.get(this.instance).wait(380).to({_off:false},0).wait(151));
	// Layer 4
	this.instance_1 = new lib.s43sf("synched",0,false);
	this.instance_1.parent = this;
	this.instance_1.setTransform(285.3,642.5,1,1,0,0,0,171.3,139.4);
	this.instance_1._off = true;
	this.timeline.addTween(cjs.Tween.get(this.instance_1).wait(229).to({_off:false},0).wait(302));
	// Layer 3
	this.instance_2 = new lib._45авап("synched",0,false);
	this.instance_2.parent = this;
	this.instance_2.setTransform(291.5,774.3,1,1,0,0,0,291.5,269.5);
	this.instance_2._off = true;
	this.timeline.addTween(cjs.Tween.get(this.instance_2).wait(79).to({_off:false},0).wait(452));
	// Layer 2
	this.instance_3 = new lib._65пкупк("synched",0,false);
	this.instance_3.parent = this;
	this.instance_3.setTransform(167,191.1,1,1,0,0,0,164.2,188.1);
	this.instance_3._off = true;
	this.timeline.addTween(cjs.Tween.get(this.instance_3).wait(9).to({_off:false},0).wait(522));
	// Isolation Mode
	this.instance_4 = new lib._4ауаа();
	this.instance_4.parent = this;
	this.instance_4.setTransform(287.1,439.8,1,1,0,0,0,80.8,55.4);
	this.timeline.addTween(cjs.Tween.get(this.instance_4).wait(531));
}).prototype = p = new cjs.MovieClip();
p.nominalBounds = new cjs.Rectangle(495.8,1083.4,165.6,114.9);
// library properties:
lib.properties = {
	width: 583,
	height: 1402,
	fps: 35,
	color: "#FFFFFF",
	opacity: 1.00,
	webfonts: {},
	manifest: [
		{src:"Fill1.png", id:"Fill1"}
	],
	preloads: []
};
})(lib = lib||{}, images = images||{}, createjs = createjs||{}, ss = ss||{}, AdobeAn = AdobeAn||{});
var lib, images, createjs, ss, AdobeAn;

var canvas, stage, exportRoot, anim_container, dom_overlay_container, fnStartAnimation;
function initAnimation() {
	canvas = document.getElementById("canvas");
	anim_container = document.getElementById("animation_container");
	dom_overlay_container = document.getElementById("dom_overlay_container");
	images = images||{};
	var loader = new createjs.LoadQueue(false);
	loader.addEventListener("fileload", handleFileLoad);
	loader.addEventListener("complete", handleComplete);
	loader.loadManifest(lib.properties.manifest);
}
function handleFileLoad(evt) {
	if (evt.item.type == "image") { images[evt.item.id] = evt.result; }
}
function handleComplete(evt) {
	//This function is always called, irrespective of the content. You can use the variable "stage" after it is created in token create_stage.
	var queue = evt.target;
	var ssMetadata = lib.ssMetadata;
	for(i=0; i<ssMetadata.length; i++) {
		ss[ssMetadata[i].name] = new createjs.SpriteSheet( {"images": [queue.getResult(ssMetadata[i].name)], "frames": ssMetadata[i].frames} )
	}
	exportRoot = new lib.index();
	stage = new createjs.Stage(canvas);
	stage.addChild(exportRoot);
	//Registers the "tick" event listener.
	fnStartAnimation = function() {
		createjs.Ticker.setFPS(lib.properties.fps);
		createjs.Ticker.addEventListener("tick", stage);
	}
	//Code to support hidpi screens and responsive scaling.
	function makeResponsive(isResp, respDim, isScale, scaleType) {
		var lastW, lastH, lastS=1;
		window.addEventListener('resize', resizeCanvas);
		resizeCanvas();
		function resizeCanvas() {
			var w = lib.properties.width, h = lib.properties.height;
			var iw = window.innerWidth, ih=window.innerHeight;
			var pRatio = window.devicePixelRatio || 1, xRatio=iw/w, yRatio=ih/h, sRatio=1;
			if(isResp) {
				if((respDim=='width'&&lastW==iw) || (respDim=='height'&&lastH==ih)) {
					sRatio = lastS;
				}
				else if(!isScale) {
					if(iw<w || ih<h)
						sRatio = Math.min(xRatio, yRatio);
				}
				else if(scaleType==1) {
					sRatio = Math.min(xRatio, yRatio);
				}
				else if(scaleType==2) {
					sRatio = Math.max(xRatio, yRatio);
				}
			}
			canvas.width = w*pRatio*sRatio;
			canvas.height = h*pRatio*sRatio;
			canvas.style.width = dom_overlay_container.style.width = anim_container.style.width =  w*sRatio+'px';
			canvas.style.height = anim_container.style.height = dom_overlay_container.style.height = h*sRatio+'px';
			stage.scaleX = pRatio*sRatio;
			stage.scaleY = pRatio*sRatio;
			lastW = iw; lastH = ih; lastS = sRatio;
		}
	}
	makeResponsive(false,'both',false,1);
	fnStartAnimation();
}