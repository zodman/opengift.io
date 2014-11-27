/**
 * Author: Vladimir Savinykh <sintez.90@gmail.com>
 * createAvatar
 * create svn avatars
 * v.001
 */
(function ( $ ) {
    $.createAvatar = function(params) {
        return '<div>'
                + '<code style="background-color: transparent;padding: 0;">'
                + '<svg viewBox="0 0 90 90">'
                + '<title>' + params.initials + '</title>'
                + '<rect rx="4" ry="4" x="0" y="0" width="90" height="90" style="fill: ' + params.color + '"/>'
                + '<g style="font-weight: bold; font-size: 67px;">'
                + '<defs><mask id="textMask' + params.id + '">'
                + '<text style="fill:white;" x="6" y="72">' + params.initials + '</text>'
                + '</mask>'
                + '<filter id="innerShadow' + params.id + '" x="-20%" y="-20%" width="140%" height="140%">'
                + '<feGaussianBlur in="SourceGraphic" stdDeviation="3" result="blur"/>'
                + '<feOffset in="blur" dx="2.5" dy="2.5"/>'
                + '</filter>'
                + '</defs>'
                + '<g mask="url(#textMask' + params.id + ')">'
                + '<rect x="0" y="0" width="90" height="90" style="fill:black"/>'
                + '<text style="fill: ' + params.color + '; filter: url(#innerShadow' + params.id + ')" x="6" y="72">'
                + params.initials + '</text></g>'
                + '</g>'
                + '</svg>'
                + '</code>'
                + '</div>'
    };
}( jQuery ));

$(document).ready(function(){
    $('.avatar_container').each(function(index,el){
        var params = $(el).attr('rel');
        if (params.length > 0) {
            $(el).append($.createAvatar(JSON.parse(params)));
        };
    })
});