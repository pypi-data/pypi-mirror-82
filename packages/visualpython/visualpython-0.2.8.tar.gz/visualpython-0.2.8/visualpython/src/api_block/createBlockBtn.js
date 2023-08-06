define([
    'nbextensions/visualpython/src/common/vpCommon'

    , './api.js'
    , './constData.js'
    , './block.js'
    , './shadowBlock.js'
], function (vpCommon, api, constData, blockData, shadowBlock ) {
    const { changeOldToNewState
            , findStateValue
            , mapTypeToName } = api;
    const { BLOCK_CODE_BTN_TYPE
            , BLOCK_CODE_TYPE
            , BLOCK_DIRECTION
            , BLOCK_TYPE
            , MAKE_CHILD_BLOCK 

            , BLOCK_HEIGHT_PX
            , INDENT_DEPTH_PX
            , MAX_ITERATION
            , NUM_ZERO
            
            , STR_TOP
            , STR_LEFT
            , STR_DIV
            , STR_BORDER
            , STR_PX
            , STR_OPACITY
            , STR_MARGIN_TOP
            , STR_MARGIN_LEFT
            , STR_DISPLAY
            , STR_BACKGROUND_COLOR
            , STR_HEIGHT
            , STR_YES
            , STR_DATA_NUM_ID 
            , STR_DATA_DEPTH_ID
            , STR_NONE
            , STR_BLOCK
            , STR_SELECTED
            , STR_COLON_SELECTED
            , STR_POSITION
            , STR_STATIC
            , STR_RELATIVE
            , STR_ABSOLUTE

            , STR_CLASS
            , STR_DEF
            , STR_IF
            , STR_FOR
            , STR_WHILE
            , STR_IMPORT
            , STR_API
            , STR_TRY
            , STR_RETURN
            , STR_BREAK
            , STR_CONTINUE
            , STR_PASS
            , STR_CODE
            , STR_ELIF

            , STR_CSS_CLASS_VP_BLOCK_CONTAINER
            , STR_CSS_CLASS_VP_BLOCK_NULLBLOCK
            , STR_CSS_CLASS_VP_BLOCK_SHADOWBLOCK
            , STR_CSS_CLASS_VP_BLOCK_DELETE_BTN
            , STR_CSS_CLASS_VP_NODEEDITOR_LEFT
            , STR_CSS_CLASS_VP_NODEEDITOR_BOTTOM_TAB_VIEW
            , STR_CSS_CLASS_VP_BLOCK_LEFT_HOLDER
            , STR_CSS_CLASS_VP_NODEEDITOR_MINIMIZE
            , STR_CSS_CLASS_VP_NODEEDITOR_ARROW_UP
            , STR_CSS_CLASS_VP_NODEEDITOR_ARROW_DOWN
            , STR_CSS_CLASS_VP_SELECTED_SHADOWBLOCK
            , STR_CHANGE_KEYUP_PASTE

            , STATE_classInParamList
            , STATE_className
            , STATE_defName
            , STATE_defInParamList
            , STATE_ifCodeLine
            , STATE_isIfElse
            , STATE_isForElse
            , STATE_elifCodeLine
            , STATE_elifList
            , STATE_forCodeLine
            , STATE_whileCodeLine
            , STATE_baseImportList
            , STATE_customImportList
            , STATE_exceptList
            , STATE_exceptCodeLine
            , STATE_isFinally
            , STATE_returnOutParamList
            , STATE_customCodeLine
            
            , COLOR_BLUE
            , COLOR_RED
            , COLOR_GREEN } = constData;  
    const {Block, mapTypeToBlock } = blockData;
    const ShadowBlock = shadowBlock;

    var CreateBlockBtn = function(blockContainerThis, type) { 
        this.blockContainerThis = blockContainerThis;
        this.state = {
            // identityNum: 100
            type
            , name: ''
            , isStart: false
            , isDroped: false
        }
        this.rootDomElement = null;

        this.mapTypeToName(type);
        this.render();
        this.bindDragEvent();
    }

    CreateBlockBtn.prototype.getBlockContainerThis = function() {
        return this.blockContainerThis;
    }

    CreateBlockBtn.prototype.setIsStart = function(isStart) {
        this.setState({
            isStart
        });
    }
    CreateBlockBtn.prototype.getIsStart = function() {
        return this.state.isStart;
    }
    CreateBlockBtn.prototype.setIsDroped = function(isDroped) {
        this.setState({
            isDroped
        });
    }
    CreateBlockBtn.prototype.getIsDroped  = function() {
        return this.state.isDroped;
    }

    CreateBlockBtn.prototype.getName = function() {
        return this.state.name;
    }

    CreateBlockBtn.prototype.setName = function(name) {
        this.setState({
            name
        });
    }
    CreateBlockBtn.prototype.getType = function() {
        return this.state.type;
    }

    CreateBlockBtn.prototype.mapTypeToName = function(type) {
        var name = ``;
        switch (type) {
            case BLOCK_CODE_TYPE.CLASS: {
                name = STR_CLASS;
                break;
            }
            case BLOCK_CODE_TYPE.DEF: {
                name = STR_DEF;
                break;
            }
            case BLOCK_CODE_TYPE.IF: {
                name = STR_IF;
                break;
            }
            case BLOCK_CODE_TYPE.FOR: {
                name = STR_FOR;
                break;
            }
            case BLOCK_CODE_TYPE.WHILE: {
                name = STR_WHILE;
                break;
            }
            case BLOCK_CODE_TYPE.IMPORT: {
                name = STR_IMPORT;
                break;
            }
            case BLOCK_CODE_TYPE.API: {
                name = STR_API;
                break;
            }
            case BLOCK_CODE_TYPE.TRY: {
                name = STR_TRY;
                break;
            }
            case BLOCK_CODE_TYPE.RETURN: {
                name = STR_RETURN;
                break;
            }
            case BLOCK_CODE_TYPE.BREAK: {
                name = STR_BREAK;
                break;
            }
            case BLOCK_CODE_TYPE.CONTINUE: {
                name = STR_CONTINUE;
                break;
            }
            case BLOCK_CODE_TYPE.PASS: {
                name = STR_PASS;
                break;
            }
            case BLOCK_CODE_TYPE.CODE: {
                name = STR_CODE;
                break;
            }

            default: {
                break;
            }
        }

        this.setState({
            name
        });
    }





    CreateBlockBtn.prototype.getMainDom = function() {
        return this.rootDomElement;
    }

    CreateBlockBtn.prototype.setMainDom = function(rootDomElement) {
        this.rootDomElement = rootDomElement;
    }
    CreateBlockBtn.prototype.getMainDomPosition = function() {
        var rootDom = this.getMainDom();
        var clientRect = $(rootDom)[0].getBoundingClientRect();
        return clientRect;
    }







    // ** Block state 관련 메소드들 */
    CreateBlockBtn.prototype.setState = function(newState) {
            this.state = changeOldToNewState(this.state, newState);
            this.consoleState();
    }
    /**
        특정 state Name 값을 가져오는 함수
        @param {string} stateKeyName
    */
    CreateBlockBtn.prototype.getState = function(stateKeyName) {
        return findStateValue(this.state, stateKeyName);
    }
    CreateBlockBtn.prototype.getStateAll = function() {
        return this.state;
    }
    CreateBlockBtn.prototype.consoleState = function() {
        // console.log(this.state);
    }






    CreateBlockBtn.prototype.render = function() {
        var blockContainer;
        var rootDomElement = $(`<div class='vp-nodeeditor-tab-navigation-node-block-body-btn'>
                                    <span class='vp-block-name'>${this.getName()}</span>
                                </div>`);
        this.setMainDom(rootDomElement);
        if (this.getType() === BLOCK_CODE_TYPE.CLASS || this.getType() === BLOCK_CODE_TYPE.DEF) {
            blockContainer = $(`.vp-nodeeditor-tab-navigation-node-subblock-1-body-inner`);
            $(rootDomElement).addClass('vp-block-class-def');
        } else if (this.getType() === BLOCK_CODE_TYPE.IF || this.getType() === BLOCK_CODE_TYPE.FOR
            || this.getType() === BLOCK_CODE_TYPE.WHILE || this.getType() === BLOCK_CODE_TYPE.TRY
            || this.getType() === BLOCK_CODE_TYPE.ELSE || this.getType() === BLOCK_CODE_TYPE.ELIF
            || this.getType() === BLOCK_CODE_TYPE.FOR_ELSE || this.getType() === BLOCK_CODE_TYPE.EXCEPT 
            || this.getType() === BLOCK_CODE_TYPE.FINALLY) {
            blockContainer = $(`.vp-nodeeditor-tab-navigation-node-subblock-2-body-inner`);
            $(rootDomElement).addClass('vp-block-if');
  
        } else {
            blockContainer = $(`.vp-nodeeditor-tab-navigation-node-subblock-3-body-inner`);
            $(rootDomElement).css(STR_BACKGROUND_COLOR, COLOR_GREEN);
     
        }

        blockContainer.append(rootDomElement);
    }



    CreateBlockBtn.prototype.bindDragEvent = function() {
        var that = this;
        var rootDom = this.getMainDom();
        var blockContainerThis = this.getBlockContainerThis();
        var createBlockBtnType = this.getType();

        var pos1 = 0;
        var pos2 = 0; 
        var pos3 = 0; 
        var pos4 = 0;
        var buttonX = 0;
        var buttonY = 0;
        var newPointX = 0;
        var newPointY = 0;
        var selectedBlockDirection;
        var shadowBlockList = [];
        $(this).addClass(`vp-nodeeditor-draggable`);
        $(rootDom).draggable({ 
            appendTo: STR_CSS_CLASS_VP_NODEEDITOR_LEFT,
        
            cursor: 'move', 
            helper: 'clone',
            start: function(event, ui) {
                var rootBlockList = blockContainerThis.getRootBlockList();
               
                rootBlockList.forEach((rootBlock, index) => {
                    var shadowBlock = new ShadowBlock(blockContainerThis, createBlockBtnType, {pointX: 0, pointY: 0}, [],  BLOCK_TYPE.SHADOW_BLOCK);
                    shadowBlock.setRootBlockUUID(rootBlock.getUUID());
                    shadowBlockList.push(shadowBlock);

                    var containerDom = rootBlock.getContainerDom();
                    $(shadowBlock.getMainDom()).css(STR_DISPLAY,STR_NONE);
                    $(shadowBlock.getMainDom()).removeClass(STR_CSS_CLASS_VP_SELECTED_SHADOWBLOCK);
                    $(containerDom).append(shadowBlock.getMainDom());
                });
                blockContainerThis.renderBlockLeftHolderListHeight();
            },
            drag: (event, ui) => {                   
                blockContainerThis.renderBlockLeftHolderListHeight();
                buttonX = event.clientX; 
                buttonY = event.clientY; 

                pos1 = pos3 - buttonX;
                pos2 = pos4 - buttonY;
                pos3 = buttonX;
                pos4 = buttonY;

                newPointX = buttonX - pos2 - $(STR_CSS_CLASS_VP_NODEEDITOR_LEFT).offset().left;
                newPointY = buttonY - pos1 - $(STR_CSS_CLASS_VP_NODEEDITOR_LEFT).offset().top;

                var blockList = blockContainerThis.getBlockList();
                blockList.forEach(block => {
                    var mainDom = block.getMainDom();
                    var { x, y, width: blockWidth, height: blockHeight} = block.getMainDomPosition();
                    var rootBlock = block.getRootBlock();
                    var blockCodeType = block.getType();
            
                    if ( x < buttonX && buttonX < (x + blockWidth)
                        && y - blockHeight/2 < buttonY && buttonY < (y + blockHeight + blockHeight) ) { 

                        if (blockCodeType === BLOCK_CODE_TYPE.NULL) {
                            return;
                        }
                        shadowBlockList.some(shadowBlock => {
                            if (shadowBlock.getRootBlockUUID() === rootBlock.getUUID()) {
                                $(shadowBlock.getMainDom()).css(STR_DISPLAY,STR_BLOCK);
                                $(shadowBlock.getMainDom()).addClass(STR_CSS_CLASS_VP_SELECTED_SHADOWBLOCK);
                                shadowBlock.setSelectBlock(block);

                                if (blockCodeType === BLOCK_CODE_TYPE.CLASS || blockCodeType === BLOCK_CODE_TYPE.DEF || blockCodeType === BLOCK_CODE_TYPE.IF ||
                                    blockCodeType === BLOCK_CODE_TYPE.FOR || blockCodeType === BLOCK_CODE_TYPE.WHILE || blockCodeType === BLOCK_CODE_TYPE.TRY || 
                                    blockCodeType === BLOCK_CODE_TYPE.FOR_ELSE || blockCodeType === BLOCK_CODE_TYPE.EXCEPT || blockCodeType === BLOCK_CODE_TYPE.FINALLY) {
         
                                    block.getNextBlockList().some(nextBlock => {
                                        if ( nextBlock.getType() === BLOCK_CODE_TYPE.NULL ) {
                                            var holderBlock = block.getHolderBlock();
                                            var blockLeftHolderHeight = block.getTempBlockLeftHolderHeight();
                                            block.getBlockLeftHolderDom().css(STR_HEIGHT, `${blockLeftHolderHeight}px`);
                                            //FIXME:
                                            // $(holderBlock.getMainDom()).css('transform', `translate(0px, -34px)`); 
                            
                                            return true;
                                        }
                                    });
                                }

                                //FIXME:
                                // if (blockCodeType === BLOCK_CODE_TYPE.HOLDER) {
                                    // $(block.getMainDom()).css('transform', `translate(0px, 0px)`); 
                                // }
                                
                                return true;
                            }
                        });
                        if (blockCodeType === BLOCK_CODE_TYPE.CLASS || blockCodeType === BLOCK_CODE_TYPE.DEF || blockCodeType === BLOCK_CODE_TYPE.IF ||
                            blockCodeType === BLOCK_CODE_TYPE.FOR || blockCodeType === BLOCK_CODE_TYPE.WHILE || blockCodeType === BLOCK_CODE_TYPE.TRY
                            || blockCodeType === BLOCK_CODE_TYPE.FOR_ELSE || blockCodeType === BLOCK_CODE_TYPE.EXCEPT || blockCodeType === BLOCK_CODE_TYPE.FINALLY) {
                            selectedBlockDirection = BLOCK_DIRECTION.INDENT;
                        } else if (block.getType() === BLOCK_CODE_TYPE.HOLDER) {
                            selectedBlockDirection = BLOCK_DIRECTION.DOWN; 
                        } else {
                            selectedBlockDirection = BLOCK_DIRECTION.DOWN; 
                     
                        }
                        rootBlock.reArrangeChildBlockDomList(block, undefined, selectedBlockDirection);
                    } else {
                        //FIXME:
                        // if (blockCodeType === BLOCK_CODE_TYPE.HOLDER) {
                            // $(block.getMainDom()).css('transform', `translate(0px, 0px)`); 
                        // }
           
                        var rootBlockList = blockContainerThis.getRootBlockList();
                        rootBlockList.some(rootBlock => {
                            var containerDom = rootBlock.getContainerDom();
                            var containerDomRect = $(containerDom)[0].getBoundingClientRect();

                            var { x, y, width: containerDomWidth, height: containerDomHeight} = containerDomRect;
                            if ( x < buttonX
                                && buttonX < (x + containerDomWidth)
                                && y  < buttonY
                                && buttonY < (y + containerDomHeight) ) {  
                                // console.log('in colision');
                            } else {
                                shadowBlockList.forEach(shadowBlock => {
                                    if (shadowBlock.getRootBlockUUID() === rootBlock.getUUID()) {
                                        $(shadowBlock.getMainDom()).removeClass(STR_CSS_CLASS_VP_SELECTED_SHADOWBLOCK);
                                        shadowBlock.setSelectBlock(null);
                                    }    
                                });
                                // console.log('not colision');
                            }
                        });
                    }
                });
            },
            stop: function() {
                var selectedBlock = null;
     
                var blockList = blockContainerThis.getBlockList();
                // blockList.forEach(block => {
                    // if (block.getType() === BLOCK_CODE_TYPE.HOLDER) {
                        // $(block.getMainDom()).css('transform', `translate(0px, 0px)`); 
                    // }
                // });

                var rootBlockList = blockContainerThis.getRootBlockList();

                shadowBlockList.forEach(shadowBlock => {
                    if ( $(shadowBlock.getMainDom()).hasClass(STR_CSS_CLASS_VP_SELECTED_SHADOWBLOCK) ) {
                        selectedBlock = shadowBlock.getSelectBlock();
                    } else {
                    };
                });

                rootBlockList.forEach(rootBlock => {
                    var rootBlockContainerDom = rootBlock.getContainerDom();
                    $(rootBlockContainerDom).find(STR_CSS_CLASS_VP_BLOCK_SHADOWBLOCK).remove();
                });

                if (selectedBlock !== null) {
                    if ((selectedBlock.getType() === BLOCK_CODE_TYPE.CLASS || selectedBlock.getType() === BLOCK_CODE_TYPE.DEF
                        || selectedBlock.getType() === BLOCK_CODE_TYPE.IF || selectedBlock.getType() === BLOCK_CODE_TYPE.FOR
                        || selectedBlock.getType() === BLOCK_CODE_TYPE.WHILE ||  selectedBlock.getType() === BLOCK_CODE_TYPE.TRY
                        || selectedBlock.getType() === BLOCK_CODE_TYPE.FOR_ELSE || selectedBlock.getType() === BLOCK_CODE_TYPE.EXCEPT 
                        || selectedBlock.getType() === BLOCK_CODE_TYPE.FINALLY)
                        && selectedBlock.getNullBlock() !== null) {
                        selectedBlock.getNullBlock().deleteBlockOne();
                        selectedBlock.setNullBlock(null);
                    } 

                    var block = mapTypeToBlock(blockContainerThis, createBlockBtnType, {pointX: 0, pointY: 0})
                    if (createBlockBtnType === BLOCK_CODE_TYPE.CLASS || createBlockBtnType === BLOCK_CODE_TYPE.DEF ) {
                        $(block.getHolderBlock().getMainDom()).css(STR_BACKGROUND_COLOR,`${COLOR_BLUE}`);
                    }
                    selectedBlock.appendBlock(block, selectedBlockDirection);

                    var rootBlock = selectedBlock.getRootBlock();
                    var x = rootBlock.getContainerPointX();
                    var y = rootBlock.getContainerPointY();
                    newPointX = x - $(STR_CSS_CLASS_VP_NODEEDITOR_LEFT).offset().left;
                    newPointY = y - $(STR_CSS_CLASS_VP_NODEEDITOR_LEFT).offset().top;
                    var containerDom = rootBlock.getContainerDom();

                    $(containerDom).css(STR_TOP,`${y}${STR_PX}`);
                    $(containerDom).css(STR_LEFT,`${x}${STR_PX}`);
                    rootBlock.setContainerPointX(x);
                    rootBlock.setContainerPointY(y);

                    block.renderResetColor();
                    block.renderClickColor();
                    block.renderBottomOption();
                    /** 생성된 BLOCK 색칠 
                     *    block.renderWhiteColor();
                    */
                }  else { 
                    var block = mapTypeToBlock(blockContainerThis, createBlockBtnType, {pointX: 0, pointY: 0});
                    /** 삭제 */
                    {
                        var containerDom = block.getContainerDom();
                        $(containerDom).empty();
                        $(containerDom).remove();
                    }
                    var containerDom = document.createElement(STR_DIV);
                    containerDom.classList.add(STR_CSS_CLASS_VP_BLOCK_CONTAINER);
                    block.setContainerDom(containerDom);

                    var blockMainDom = block.getMainDom();
                    $(containerDom).append(blockMainDom);

                    block.setContainerPointX(newPointX);
                    block.setContainerPointY(newPointY);

                    $(containerDom).css(STR_TOP,`${newPointY}${STR_PX}`);
                    $(containerDom).css(STR_LEFT,`${newPointX}${STR_PX}`);

                    if (createBlockBtnType === BLOCK_CODE_TYPE.CLASS || createBlockBtnType === BLOCK_CODE_TYPE.DEF 
                        || createBlockBtnType === BLOCK_CODE_TYPE.IF ||
                        createBlockBtnType === BLOCK_CODE_TYPE.FOR || createBlockBtnType === BLOCK_CODE_TYPE.WHILE 
                        || createBlockBtnType === BLOCK_CODE_TYPE.TRY
                        || createBlockBtnType === BLOCK_CODE_TYPE.FOR_ELSE || createBlockBtnType === BLOCK_CODE_TYPE.EXCEPT 
                        || createBlockBtnType === BLOCK_CODE_TYPE.FINALLY) {
               
                        $(containerDom).append(block.getNullBlock().getMainDom());

                        if (createBlockBtnType === BLOCK_CODE_TYPE.CLASS || createBlockBtnType === BLOCK_CODE_TYPE.DEF ) {
                            $(block.getHolderBlock().getMainDom()).css(STR_BACKGROUND_COLOR,`${COLOR_BLUE}`);
                        }

                        $(containerDom).append(block.getHolderBlock().getMainDom());
            
                        block.bindDragEvent();
                        block.bindClickEvent();
                    }
                    $(STR_CSS_CLASS_VP_NODEEDITOR_LEFT).append(containerDom);
                    block.renderResetColor();
                    block.renderClickColor();
                    block.renderBottomOption();
                }

                var blockList = blockContainerThis.getBlockList();
                blockList.forEach(block => {
                    if (block.getNullBlock()) {
                        $(block.getNullBlock().getMainDom()).css(STR_DISPLAY, STR_BLOCK); 
                    }
                    var mainDom = block.getMainDom();
                    $(mainDom).find(STR_CSS_CLASS_VP_BLOCK_DELETE_BTN).remove();
                });
                // var blockList = blockContainerThis.getBlockList();
                // blockList.forEach((block, index) => {
                //     if ( block.getNullBlock() ) {
                //         $(block.getNullBlock().getMainDom()).css(STR_DISPLAY,STR_BLOCK); 
                //     }
                // });
                blockContainerThis.renderBlockLeftHolderListHeight();
                /** 메모리에 남은 shadowBlockList 삭제 */
                shadowBlockList = [];
            }
        });
    }

    return CreateBlockBtn;
});
