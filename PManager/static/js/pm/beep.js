/**
 * Created with PyCharm.
 * User: Gvammer
 * Date: 15.07.14
 * Time: 16:18
 */
var beep = (function () {
    var ctx = new(window.audioContext || window.webkitAudioContext);
    if (!ctx) return false;
    return function (duration, type, finishedCallback) {

        duration = +duration;

        // Only 0-4 are valid types.
        type = (type % 5) || 0;

        if (typeof finishedCallback != "function") {
            finishedCallback = function () {};
        }

        var osc = ctx.createOscillator();

        osc.type = type;

        osc.connect(ctx.destination);
        osc.noteOn(0);

        setTimeout(function () {
            osc.noteOff(0);
            finishedCallback();
        }, duration);

    };
})();