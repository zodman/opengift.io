/**
 * Created with PyCharm.
 * User: Gvammer
 * Date: 27.07.14
 * Time: 17:22
 */

var cTimeThumb = function (params) {
    if (params.container)
        this.$container = $(params.container);
    this.containerWidth = this.$container.width();// - 15;

    this.dateStart = params.dateStart;
    this.dateEnd = params.dateEnd;
    this.$scrollWin = $(params.scrollWin);
    this.$progressContainer = this.$container.find('.dates-subtasks');
    this.thumbScale = 0.2;
    this.minWidthScroll = 5;
    this.marginScrollRight = 0;
    this.posScrollTimer = false;
    this.dragWinFlag = false;
    this.padding = 0;//22
    this.big = params.big;

    this.getWinLeft = function () {
        return this.$scrollWin.css('left').replace('px', '') * 1;
    }

//    this.getContainerLeft = function () {
//        return this.$container.css('left').replace('px', '') * 1;
//    }

    this.drawLabels = function () {
        var curDate = new Date(this.big.startDate),
            endDate = new Date(this.big.endDate);
        this.$container.find('.dates-bar').empty();
        while ((endDate - curDate) > 0) {
            curDate = new Date(Date.UTC(curDate.getUTCFullYear(), curDate.getUTCMonth() + 1, 0));
            var curLeft = this.big.msToPx(this.big.stripTime(curDate)) * this.thumbScale;
            curDate = new Date(Date.UTC(curDate.getUTCFullYear(), curDate.getUTCMonth() + 1, 1));
            this.$container.find('.dates-bar').append(
                '<div class="dates-bar-item" style="left: ' + (curLeft - 90) + 'px;">' +
                    '<span class="dates-bar-item-border"></span>' +
                    this.big.monthNames[curDate.getUTCMonth()] +
                    '</div>'
            );
        }
        return this;
    }

    this.drawEvents = function () {
        var t = this;
        t.$container.find('.planlet-container').empty();
//        <div class="marker category3" style="left:150px; top:18px"></div>
        for (var row = 0; row < t.big.eventRows.length; row++) {
            arTimers = [];
            var upperY = ((5 - row) > 0 ? 5 - row : 1) * 3;
            for (var col = 0; col < t.big.eventRows[row].length; col++) {
                var event = t.big.eventRows[row][col];
                var startX = (event.dates[0].getTime() - t.big.startTime) * t.big.pxRatio * t.thumbScale;
                var elem = null;
                var width = (t.big.getEndDate(event.dates) - event.dates[0]) * t.big.pxRatio * t.thumbScale;
                t.$container.find('.planlet-container').append(
                    '<div class="marker category' + (event.closed ? '1' : '3') + '" style="left:' + startX + 'px; top:' + upperY + 'px"></div>'
                );
            }
        }
        return this;
    }

    this.drawMilestones = function () {
        var t = this;
        var l = t.big.milestones.length;
        for (var i = 0; i < l; i++) {
            var milestone = t.big.milestones[i];
            var left = (milestone.date.getTime() - t.big.startDate.getTime()) / (t.big.endDate.getTime() - t.big.startDate.getTime());

            var leftInPx = Math.round(left * t.allProjectWidth, 2);
            var $milestone = $('<a></a>', {
                'class': 'fa fa-star mini milestone-mini',
                'href': '#',
                'title': milestone.name,
                'data-id': milestone.id
            });
            $milestone.appendTo(t.$progressContainer.find('.js-stars'));
            $milestone.css('left', leftInPx);
            if (milestone.closed) {
                $milestone.addClass('green');
            } else {
                $milestone.addClass('red');
            }

            //go to milestone on click
            (function (t, $milestone, left) {
                $milestone.click(function () {
                    t.big.goToPx(-Math.round(left * t.big.totalWidth - (t.big.visibleWidth / 2)));
                    t.synchronize();
                    return false;
                });
            })(t, $milestone, left);
        }
        return this;
    }

//    this.getThumbWinPosition = function () {
//        var left = 0;
//        return left;
//    }

    this.synchronize = function () {
        var t = this;
        t.$container = $('div.diagramma').eq(0);//todo: разобраться с проблемой
        t.scrollWinLeft = t.big.msToPx(t.big.getLeftTime()) * t.thumbScale + t.allProjectLeft;
//        if (t.scrollWinLeft < t.padding) {
//            t.allProjectLeft = t.allProjectLeft - (t.scrollWinLeft);
//            t.scrollWinLeft = t.padding - 2;
//            t.$progressContainer.css('left', t.allProjectLeft + t.padding - 1);
//        } else if (t.scrollWinLeft > t.containerWidth - this.$scrollWin.width() - t.marginScrollRight) {
//            t.allProjectLeft = t.allProjectLeft - (t.scrollWinLeft + this.$scrollWin.width() + 1 - t.containerWidth);
//            t.scrollWinLeft = t.containerWidth - this.$scrollWin.width() - t.marginScrollRight;
//            t.$progressContainer.css('left', t.allProjectLeft);
//        }
        t.$scrollWin.css('left', t.scrollWinLeft);
    }

    this.init = function () {
        var t = this;
        t.allProjectWidth = t.$progressContainer.width();// * t.thumbScale;
        t.thumbScale = t.allProjectWidth / t.big.totalWidth;
        t.scrollWinWidth = t.allProjectWidth * t.big.visibleWidth / t.big.totalWidth;
        t.allProjectLeft = 0;//t.big.getLeftPx() * t.thumbScale;//TODO: найти правильную формулу
        t.scrollWinLeft = t.big.msToPx(t.big.getLeftTime()) * t.thumbScale + t.allProjectLeft - 7;//ушки у прозрачного окошка
//        t.$progressContainer.css('width',t.allProjectWidth);
        t.$progressContainer.css('left', t.allProjectLeft);
        t.$scrollWin.css('width', t.scrollWinWidth);
        t.$scrollWin.css('left', t.scrollWinLeft);
        t.dragWinLeft = t.getWinLeft();
        t.drawEvents().drawLabels().drawMilestones();
        t.resizeOnePxZoom = t.big.visibleSpan / t.scrollWinWidth;
        t.maxProjectLeft = t.allProjectWidth - t.containerWidth;
        this.$progressContainer.find(".bar").width(t.big.msToPx(t.big.nowTime.getTime()) * t.thumbScale);
        this.$scrollWin.unbind('.mousedown.timethumb .touchstart.timethumb').bind('mousedown.timethumb touchstart.timethumb', function (e) {
            if (event.type === 'touchstart') {
                e = e.originalEvent.touches[0] || e.originalEvent.changedTouches[0];
            }
            e = fixEvent(e);
            t.dragWinFlag = true;
            t.mouseX = e.pageX;
            t.big.dragPaperStart = t.big.getLeftPx();
            t.dragWinLeft = t.getWinLeft();

        });
        $('.js-goToNow').click(function () {
            var nowTime = t.big.stripTime(new Date());
            t.big.goToDate(nowTime);
            return false;
        });

        $(document).find(".scroll-bar-left").unbind('.mousedown.timethumb .touchstart.timethumb').bind('mousedown.timethumb touchstart.timethumb', function (e) {
            if (event.type === 'touchstart') {
                e = e.originalEvent.touches[0] || e.originalEvent.changedTouches[0];
            }
            e = fixEvent(e);
            event.stopPropagation();
            t.dragLeftFlag = true;
            t.ScrollBarLeftmouseX = e.pageX;
            t.resizeWidth = t.$scrollWin.width();
            t.resizeLeft = t.getWinLeft();
            t.resizeShift = 0;
            return false;
        });

        $(document).find(".scroll-bar-right").unbind('.mousedown.timethumb .touchstart.timethumb').bind('mousedown.timethumb touchstart.timethumb', function (e) {
            if (event.type === 'touchstart') {
                e = e.originalEvent.touches[0] || e.originalEvent.changedTouches[0];
            }
            e = fixEvent(e);
            event.stopPropagation();
            t.dragRightFlag = true;
            t.ScrollBarLeftmouseX = e.pageX;
            t.resizeWidth = t.$scrollWin.width();
            t.resizeRight = t.$scrollWin.css("right").replace('px', '') * 1;
            t.resizeShift = 0;
            return false;
        });

        $(document)
            .unbind('mouseup.timethumb touchend.timethumb mousemove.timethumb touchmove.timethumb')
            .bind('mouseup.timethumb touchend.timethumb',function () {

            t.dragWinFlag = false;
            t.dragRightFlag = false;
            if (t.resizeZoom) {
                t.zoomSize = t.$scrollWin.width() / t.allProjectWidth;

                t.big.visibleSpan = (t.big.endDate.getTime() - t.big.startDate.getTime()) * t.zoomSize;

                t.big.drawnStartMs = null;
                t.big.redraw(function () {
                    setTimeout(function() {
                        t.thumbScale = t.allProjectWidth / t.big.totalWidth;
                        t.big.goToPx(- t.getWinLeft() / t.thumbScale, false, false, true);
                    }, 600);
                });

                t.resizeZoom = false;
//                t.resizeSizeZoom = t.$scrollWin.width() * t.resizeOnePxZoom;
//                setTimeout(function () {
//                    t.dragWinFlag = true;
//                    $(document).trigger('mousemove.timethumb');
//                    t.dragWinFlag = false;
//                }, 10);

            }
            t.dragLeftFlag = false;
//            t.PosMousemoveScrollPageX = false;

//            clearInterval(t.posScrollTimer);
//            t.PosMousemoveScrollPageX = false;
//            t.posScrollTimer = false;
        }).bind('mousemove.timethumb touchmove.timethumb', function (e) {
                if (event.type === 'touchmove') {
                    e = e.originalEvent.touches[0] || e.originalEvent.changedTouches[0];
                }
                if (t.dragLeftFlag) {
                    e = fixEvent(e);
                    t.resizeShift = e.pageX - t.ScrollBarLeftmouseX;
                    var tempSdvig = t.resizeShift;
                    if (tempSdvig < 0) {
                        tempSdvig = -tempSdvig;
                    }

                    if (t.resizeShift) {
                        if (t.resizeShift < 0 && t.getWinLeft() > t.padding) {
                            t.$scrollWin.css({'left': t.resizeLeft - tempSdvig + 'px'});
                            t.$scrollWin.css({'width': t.resizeWidth + tempSdvig + 'px'});
                            t.scrollWinLeft = t.resizeLeft - tempSdvig;
                            t.dragWinLeft = t.getWinLeft();
                            t.resizeZoom = true;
                        } else if (t.resizeShift > 0 && t.$scrollWin.width() > t.minWidthScroll) {
                            t.$scrollWin.css({'left': t.resizeLeft + tempSdvig + 'px'});
                            t.$scrollWin.css({'width': t.resizeWidth - tempSdvig + 'px'});
                            t.scrollWinLeft = t.resizeLeft + tempSdvig;
                            t.dragWinLeft = t.getWinLeft();
                            t.resizeZoom = true;
                        }
                    }
                }
                if (t.dragRightFlag) {
                    e = fixEvent(e);
                    t.resizeShift = e.pageX - t.ScrollBarLeftmouseX;
                    var tempSdvig = t.resizeShift;
                    if (tempSdvig > 0) {
                        tempSdvig = -tempSdvig;
                    }
                    if (t.resizeShift) {
                        if (t.resizeShift < 0 && t.$scrollWin.width() > t.minWidthScroll) {//this.minWidthScroll  - минимальная ширина скрола
                            t.$scrollWin.css({'width': t.resizeWidth + tempSdvig + 'px'});
                            t.resizeZoom = true;
                        } else if (t.resizeShift > 0 && (t.$scrollWin.width() + (t.getWinLeft()) + t.padding) < t.$container.width()) {
                            t.$scrollWin.css({'width': t.resizeWidth - tempSdvig + 'px'});
                            t.resizeZoom = true;
                        }
                    }
                }

                if (t.dragWinFlag) {
                    e = fixEvent(e);
                    var offsetX = e.pageX - t.mouseX;
                    if (offsetX) {
                        var offsetExists = false;
//                        if (offsetX < 0 && t.allProjectLeft >= 0 && t.scrollWinLeft <= t.allProjectLeft) {
//                            offsetX = t.allProjectLeft - t.scrollWinLeft;
//                        } else if (offsetX > 0 && (t.allProjectLeft + t.allProjectWidth <= t.containerWidth) && t.scrollWinLeft >= t.allProjectLeft + t.allProjectWidth - t.$scrollWin.width()) {
//                            offsetX = t.containerWidth - t.allProjectLeft + t.allProjectWidth - t.scrollWinLeft;
//                        }

                        if (true ||
                            (offsetX < 0 && t.getWinLeft() - t.padding - 1 > 0) ||
                            (offsetX > 0 && t.getWinLeft() < t.containerWidth - t.$scrollWin.width() - 7)) {
                            //Сдвиг при условии что не у края
                            t.scrollWinLeft = t.dragWinLeft + offsetX;
                            if (t.scrollWinLeft < t.padding - 1) {
                                t.scrollWinLeft = t.padding - 1;
                            }
                            if (t.scrollWinLeft > t.containerWidth - t.$scrollWin.width() - t.marginScrollRight) {
                                t.scrollWinLeft = t.containerWidth - t.$scrollWin.width() - t.marginScrollRight;
                            }
//                            if (t.PosMousemoveScrollPageX && e.pageX > t.PosMousemoveScrollPageX) {//если сдвиг остановлен то останавливаем и таймер
////                                clearInterval(t.posScrollTimer);
//                                t.PosMousemoveScrollPageX = false;
////                                t.posScrollTimer = false;
//                            }
//                            if (!t.PosMousemoveScrollPageX) {
                            t.$scrollWin.css({'left': t.scrollWinLeft + 'px'});
//                                t.big.goToPx(t.big.dragPaperStart - (offsetX / t.thumbScale), false, false, true);
                            t.big.goToPx(- t.getWinLeft() / t.thumbScale, false, false, true);
                            t.mouseX = e.pageX;
                            t.dragWinLeft = t.getWinLeft();
                            t.big.dragPaperStart = t.big.getLeftPx();
//                            }
                        } else {
//                            t.currentMouseX = e.pageX;
//                            //Сдвиг при условии что  у края
//                            var projectOffset = t.allProjectLeft - offsetX;
//                            if (t.PosMousemoveScrollPageX && t.scrollWinLeft <= 0 && e.pageX + 10 > t.PosMousemoveScrollPageX || //перестать сдвигать если
//                                t.PosMousemoveScrollPageX && t.scrollWinLeft >= 0 && e.pageX - 10 < t.PosMousemoveScrollPageX
//                                ) {//если сдвиг остановлен то останавливаем и таймер
//                                clearInterval(t.posScrollTimer);
//                                t.PosMousemoveScrollPageX = false;
//                                t.posScrollTimer = false;
//                            } else if ((projectOffset < t.scrollWinLeft && offsetX < 0) || ((projectOffset > -(t.allProjectWidth - t.containerWidth)) && offsetX > 0)) {
//                                if (!t.PosMousemoveScrollPageX) {//проверка работает ли в данный момент сдвиг
//                                    t.PosMousemoveScrollPageX = e.pageX;
//
//                                    if (!t.posScrollTimer) { //если можно сдвигать и таймер не запущен то начинаем сдвиг
//                                        t.posScrollTimer = setInterval(function () {
//                                            if (t.dragWinFlag &&
//                                                t.allProjectLeft <= t.scrollWinLeft + 21 && offsetX < 0 || (-t.allProjectLeft + t.containerWidth) < t.allProjectWidth && offsetX > 0) {//бага выполняется условие когда какимто образом она сдвигается болше чем нужно
//                                                t.allProjectLeft = t.allProjectLeft - offsetX;
//                                                if (t.allProjectLeft > t.scrollWinLeft) {
//                                                    t.allProjectLeft = t.scrollWinLeft;
//                                                } else if (-t.allProjectLeft > t.allProjectWidth - t.containerWidth && offsetX > 0) {
//                                                    t.allProjectLeft = -(t.allProjectWidth - t.containerWidth + t.marginScrollRight);
//                                                }
//                                                t.$progressContainer.css('left', t.allProjectLeft);
//                                                t.big.goToPx(t.big.dragPaperStart - (offsetX / t.thumbScale), false, false, true);
//                                                t.dragWinLeft = t.getWinLeft();
//                                                t.big.dragPaperStart = t.big.getLeftPx();
//                                            } else {//если сдвигать уже некуда то останавливаем
//                                                clearInterval(t.posScrollTimer);
//                                                t.PosMousemoveScrollPageX = false;
//                                                t.posScrollTimer = false;
//                                            }
//                                        }, 30);
//                                    }
//                                }
//                            }
                        }
                    }
                }
            });
    }

    this.init();
    return this;
}