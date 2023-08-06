define([
    'nbextensions/visualpython/src/common/vpCommon'

    , './api.js'
    , './constData.js'
    , './shadowBlock.js'
    , './blockRenderer.js'
], function (vpCommon, api, constData, shadowBlock, blockRenderer ) {
    const ShadowBlock = shadowBlock;
    const { changeOldToNewState
            , findStateValue
            , mapTypeToName } = api;
    const { renderMainDom
            , renderMainInnerDom
            , renderMainHeaderDom
            , renderBottomOptionContainer
            , renderBottomOptionContainerInner
            , renderDomContainer
            , renderBottomOptionInnerDom
            , renderBottomOptionName
            , renderInParamContainer
            , renderInParamDom
            , renderBottomOptionTitle
            , renderElseBlock
            , renderDefaultOrDetailButton
            , generateClassInParamList
            , generateDefInParamList
            , generateReturnOutParamList } = blockRenderer;
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

    var Block = function(blockContainerThis, type, pointObj) {
        this.state = {
            type
            , blockType: 1
            , name: ''
            , pointX: pointObj.pointX 
            , pointY: pointObj.pointY
            , containerPointX: 0
            , containerPointY: 0
            , opacity: 1
            , isRootBlock: false
            , uuid: vpCommon.getUUID()
            , direction: BLOCK_DIRECTION.ROOT
            , tempDepth: 0
            , tempBlockLeftHolderHeight: 0
            , optionState: {
                classState: {
                    className: ''
                    , classInParamList: []
                    , selfVariableList: []
                    , methodList: []
                    , init: {
                        isClassInit: false
                        , initParamList: []
                    }
                    , del: {
                        isClassDel: false
                        , delParamList: []
                    }
                }
                , defState: {
                    defName: ''
                    , defInParamList: []
                    , defOutParamList: []
                }
                , ifState: {
                    if: {
                        ifCodeLine: ''
                    }
                    , elifList: []
                    , ifElse: {
                        isIfElse: false
                        , ifElseBlock: null
                    }
                    
                }
                , forState: {
                    for: {
                        forCodeLine: ''
                    }
                    , forElse: {
                        isForElse: false
                    }
                }
                , whileState: {
                    while: {
                        whileCodeLine: ''
                    }
                }
                , tryState: {
                    try: {
            
                    }
                    , exceptList: []
                    , finally: {
                        isFinally: false
                    }
                }
                , importState: {
                    baseImportList: [
                        baseImportNumpy = {
                            isImport: false
                            , baseImportName: 'numpy' 
                            , baseAcronyms: 'np' 
                        }   
                        , baseImportPandas = {
                            isImport: false
                            , baseImportName: 'pandas' 
                            , baseAcronyms: 'pd' 
                        }
                        , baseImportMatplotlib = {
                            isImport: false
                            , baseImportName: 'matplotlib.pyplot' 
                            , baseAcronyms: 'plt' 
                        }
                        , baseImportSeaborn= {
                            isImport: false
                            , baseImportName: 'seaborn' 
                            , baseAcronyms: 'sns' 
                        }
                        , baseImportOs= {
                            isImport: false
                            , baseImportName: 'os' 
                            , baseAcronyms: 'os' 
                        }
                        , baseImportSys= {
                            isImport: false
                            , baseImportName: 'sys' 
                            , baseAcronyms: 'sys' 
                        }
                        , baseImportTime= {
                            isImport: false
                            , baseImportName: 'time' 
                            , baseAcronyms: 'time' 
                        }
                        , baseImportDatetime= {
                            isImport: false
                            , baseImportName: 'datetime' 
                            , baseAcronyms: 'datetime' 
                        }
                        , baseImportRandom= {
                            isImport: false
                            , baseImportName: 'random' 
                            , baseAcronyms: 'random' 
                        }
                        , baseImportMath= {
                            isImport: false
                            , baseImportName: 'math' 
                            , baseAcronyms: 'math' 
                        }
                    ]
                    , customImportList: []
                }
                , elifState: {
                    elifCodeLine: ''
                }
                , exceptState :{
                    exceptCodeLine: ''
                }
                , returnState: {
                    returnOutParamList: []
                }
                , codeState: {
                    customCodeLine: ''
                }
            }
        }

        this.nextBlockList = [];
        this.blockContainerThis = blockContainerThis;

        this.rootDom = null;
        this.containerDom = null;
        this.blockLeftHolderDom = null;

        this.prevBlock = null;
        this.shadowBlock = null;
        this.nullBlock = null;
        var name = mapTypeToName(type);
        this.setName(name);

        this.init();

        var blockCodeType = this.getType();
        if (blockCodeType === BLOCK_CODE_TYPE.CLASS || blockCodeType === BLOCK_CODE_TYPE.DEF || blockCodeType === BLOCK_CODE_TYPE.IF ||
            blockCodeType === BLOCK_CODE_TYPE.FOR || blockCodeType === BLOCK_CODE_TYPE.WHILE || blockCodeType === BLOCK_CODE_TYPE.TRY ||
            blockCodeType === BLOCK_CODE_TYPE.ELSE || blockCodeType === BLOCK_CODE_TYPE.ELIF || blockCodeType === BLOCK_CODE_TYPE.FOR_ELSE || 
            blockCodeType === BLOCK_CODE_TYPE.EXCEPT || blockCodeType === BLOCK_CODE_TYPE.FINALLY ) {
            var nullBlock = mapTypeToBlock(this.blockContainerThis, BLOCK_CODE_TYPE.NULL, {pointX: 0, pointY: 0});
            var holderBlock = mapTypeToBlock(this.blockContainerThis, BLOCK_CODE_TYPE.HOLDER, {pointX: 0, pointY: 0});
            
            this.setHolderBlock(holderBlock);
            this.setNullBlock(nullBlock);
            holderBlock.setSupportingBlock(this);

            this.appendBlock(holderBlock, BLOCK_DIRECTION.DOWN);
            this.appendBlock(nullBlock, BLOCK_DIRECTION.INDENT);
        }


        this.blockContainerThis.addBlock(this);
    }

    Block.prototype.init = function() {
        var blockCodeType = this.getType();

        {
            var mainDom = this.getMainDom();
            $(mainDom).remove();
            $(mainDom).empty();
        }

        var mainDom = renderMainDom();
        mainDom = this.renderBlockLeftHolderDom(mainDom, BLOCK_TYPE.BLOCK);

        if (blockCodeType === BLOCK_CODE_TYPE.HOLDER) {
            mainDom.classList.add('vp-block-bottom-holder');
        }

        var mainInnerDom = renderMainInnerDom();
        var mainHeaderDom = renderMainHeaderDom(this);

        $(mainInnerDom).append(mainHeaderDom);          
        $(mainDom).append(mainInnerDom);
    
        this.setMainDom(mainDom);

        if (blockCodeType === BLOCK_CODE_TYPE.NULL) {
            $(mainDom).css(STR_OPACITY,'0');
            $(mainDom).addClass('vp-block-nullblock');
            $(mainDom).attr(STR_DATA_NUM_ID,`-10000`);
        }

        $(STR_CSS_CLASS_VP_NODEEDITOR_LEFT).append(mainDom);

        this.bindEventAll();
    }





    // ** --------------------------- Block을 삭제, 수정, 불러오기 혹은 주변 block과의 관계를 규정하는 메소드들 --------------------------- */

    Block.prototype.getPrevBlock = function() {
        return this.prevBlock
    }
    Block.prototype.setPrevBlock = function(prevBlock) {
        this.prevBlock = prevBlock;
    }
    Block.prototype.addNextBlockList = function(nextBlock) {
        this.nextBlockList = [ ...this.nextBlockList, nextBlock]
    }
    Block.prototype.setNextBlockList = function(nextBlockList) {
        this.nextBlockList = nextBlockList;
    }
    Block.prototype.getNextBlockList = function() {
        return this.nextBlockList;
    }
    Block.prototype.setHolderBlock = function(holderBlock) {
        this.holderBlock = holderBlock;
    }
    Block.prototype.getHolderBlock = function() {
        return this.holderBlock;
    }
    Block.prototype.setSupportingBlock = function(supportingBlock) {
        this.supportingBlock = supportingBlock;
    }
    Block.prototype.getSupportingBlock = function() {
        return this.supportingBlock;
    }
    Block.prototype.setNullBlock = function(nullBlock) {
        this.nullBlock = nullBlock;
    }
    Block.prototype.getNullBlock = function() {
        return this.nullBlock;
    }

    Block.prototype.untactBlock = function(x,y) {
        // this블록의 이전 블록이 있다면 데이터 상에서 삭제한다
        var prevBlock = this.getPrevBlock();
        if ( prevBlock ) {
            var nextBlockList = prevBlock.getNextBlockList();
            nextBlockList.some(( block, index) => {
                if (block.getUUID() === this.getUUID()) {
                    nextBlockList.splice(index, 1);
                    this.setPrevBlock(null);
                    return true;
                }
            });
            prevBlock.setNextBlockList(nextBlockList);
        }
        this.setPrevBlock(null);
        this.setDirection(BLOCK_DIRECTION.ROOT);

        this.reRender();

        var rootBlock = this.getRootBlock();
        var containerDom = rootBlock.getContainerDom();
        $(containerDom).css(STR_TOP,`${y}` + STR_PX);
        $(containerDom).css(STR_LEFT,`${x}` + STR_PX);
        $(containerDom).empty();


        rootBlock.setContainerDom(containerDom);

        var childBlockList = rootBlock.renderChildBlockListIndentAndGet();
        childBlockList.forEach((block, index) => {
            var mainDom = block.getMainDom();
            $(mainDom).css(STR_TOP,`${0}` + STR_PX);
            $(mainDom).css(STR_LEFT,`${0}` + STR_PX);
            $(mainDom).attr(STR_DATA_NUM_ID,`${index}`);
            $(containerDom).append(mainDom);

            block.bindEventAll();
        });
    }

    /** 트리 구조속의 최상위 루트 block 가져오기 */
    Block.prototype.getRootBlock = function() {
        var rootBlock = null;
        var prevBlock = this.getPrevBlock();

        var _iteration = 0;
        while (prevBlock !== null) {
            /** FIXME: 무한루프 체크 */
            if (_iteration > MAX_ITERATION) {
                console.log('무한루프');
                break;
            }
            _iteration++;
            var _prevBlock = prevBlock.getPrevBlock();
            if (_prevBlock === null) {
                rootBlock = prevBlock;
                break;
            }
            prevBlock = _prevBlock;
        }

        if (_iteration === 0) {
            rootBlock = this;
        }
        return rootBlock;
    }

    Block.prototype.getRootBlockList = function() {
        var blockContainerThis = this.getBlockContainerThis();
        var blockList = blockContainerThis.getBlockList();

        var rootBlockList = [];
        // root block 묶음 별로 분리
        blockList.forEach(block => {
            var rootBlock = block.getRootBlock();
            if (rootBlockList.includes(rootBlock)) {
            } else {
                rootBlockList.push(rootBlock);
            }
        });
        return rootBlockList;
    }

    Block.prototype.selectRootToChildBlockList = function() {
        var rootBlock = this.getRootBlock();
        return rootBlock.selectChildBlockList();
    }

    Block.prototype.selectChildBlockList = function() {
        var nextBlockList = this.getNextBlockList();
        var stack = [];

        if (nextBlockList.length !== 0) {
            stack.push(nextBlockList);
        }

        var travelBlockList = [this];

        var iteration = 0;
        var current;
        while (stack.length !== 0) {
            current = stack.shift();
            /** FIXME: 무한루프 체크 */
            if (iteration > 100) {
                console.log('무한루프');
                break;
            }
            iteration++;
            /** 배열 일 때 */
            if (Array.isArray(current)) {
                var currBlockList = current;
                var tempList = [];
                currBlockList.forEach(block => {
                    tempList.push(block);
                });
                
                tempList = tempList.sort((a,b) => {
                    if (a.getDirection() === BLOCK_DIRECTION.INDENT) {
                        return 1;
                    } else {
                        return -1;
                    }
                });
                tempList.forEach(el => {
                    stack.unshift(el);
                });


            } else {
                var currBlock = current;
                var is = travelBlockList.some(travelBlock => {
                    if (current.getUUID() === travelBlock.getUUID()) {
                        return true;
                    }
                });
                if(is === false) {
                    travelBlockList.push(currBlock);
                    var nextBlockList = currBlock.getNextBlockList();
                    stack.unshift(nextBlockList);
                }
            }
        }

        return travelBlockList;
    }

    Block.prototype.appendBlock = function(appendedBlock, direction) {
        appendedBlock.setDirection(direction);

        var prevBlock = appendedBlock.getPrevBlock();
        if ( prevBlock ) {
            var nextBlockList = prevBlock.getNextBlockList();
            nextBlockList.some(( nextBlock, index) => {
                if (nextBlock.getUUID() === appendedBlock.getUUID()) {
                    nextBlockList.splice(index, 1);
                    return true;
                }
            });
        }

        // 새로 들어온 block의 이전 블록을 현재 this블록으로 정함
        appendedBlock.setPrevBlock(this);

        var nextBlockList = this.getNextBlockList();

        if (direction === BLOCK_DIRECTION.DOWN) {
            if (nextBlockList.length !== 0) {
                var selectChildBlockList = appendedBlock.selectChildBlockList();
                selectChildBlockList[selectChildBlockList.length - 1].setNextBlockList([...nextBlockList]);
            }
    
            nextBlockList.forEach(block => {
                if (block.getDirection() === BLOCK_DIRECTION.INDENT) {
                    block.setPrevBlock(appendedBlock);
                    return true;
                }
                if (block.getDirection() === BLOCK_DIRECTION.BOTTOM_DOWN) {
                    block.setPrevBlock(appendedBlock);
                    return true;
                }
                if (block.getDirection() === BLOCK_DIRECTION.DOWN) {
                    block.setPrevBlock(appendedBlock);
                    return true;
                }            
            });
            this.setNextBlockList([appendedBlock]);  
        } else if (direction === BLOCK_DIRECTION.INDENT) {
            nextBlockList.some((nextBlock, index ) => {
                if (nextBlock.getDirection() === direction) {
                    // 새로 들어온 block이 기존에 자리잡고 있던 블록을 자식으로 append
                    nextBlock.setDirection(BLOCK_DIRECTION.DOWN);
                    appendedBlock.addNextBlockList(nextBlock);
                    // 기존에 자리잡고 있던 블록이 새로 들어온 block에 밀려남
                    nextBlock.setPrevBlock(appendedBlock);
                    nextBlockList.splice(index, 1);
                    return true;
                }

            });
            this.addNextBlockList(appendedBlock);  
        } else {
            var currBlock = this.getRootBlock();
            var nextBlockList = currBlock.getNextBlockList();
            // var iter = 0;
            while (nextBlockList.length !== 0) {
                // if (iter > 100) {
                //     console.log('무한루프');
                //     break;
                // }
                // iter++;

                var is = nextBlockList.some(block => {
                    if (block.getDirection() === BLOCK_DIRECTION.DOWN) {
                        currBlock = block;
                        return true;
                    } else {
                        return false;
                    }
        
                });

                if (is === true) {
                    nextBlockList = currBlock.getNextBlockList();
                } else {
                    break;
                }
            }
            currBlock.addNextBlockList(appendedBlock);  
            appendedBlock.setPrevBlock(currBlock);
        }

        this.reRender();
    }

    Block.prototype.splitBlockList = function() {
        // var rootBlock = this.getRootBlock();
        var currBlock = this;
        var rootToChildBlockList = this.selectRootToChildBlockList();
        var splitBlockListIndex = 0;

        rootToChildBlockList.some((block, index) => {
            if (block.getUUID() === currBlock.getUUID()) {
                splitBlockListIndex = index;
                return true;
            }
        });
        
        var beforeBlockList = rootToChildBlockList.slice(0, splitBlockListIndex);
        var afterBlockList = rootToChildBlockList.slice(splitBlockListIndex, rootToChildBlockList.length);

        return {
            beforeBlockList
            , afterBlockList
            , splitBlockListIndex
        };
    }
    Block.prototype.getShadowBlock = function() {
        return this.shadowBlock;
    }
    Block.prototype.setShadowBlock = function(shadowBlock) {
        this.shadowBlock = shadowBlock;
    }
    Block.prototype.deleteBlock = function() {
        var blockContainerThis = this.getBlockContainerThis();
        /** 렌더링된 rootDomElement 삭제 제거 */
        var rootDomElement = this.getMainDom();
        $(rootDomElement).remove();
        $(rootDomElement).empty();

        /** 부모 에서 this를 제거  */
        var prevBlock = this.getPrevBlock();
        if ( prevBlock ) {
            var nextBlockDataList = prevBlock.getNextBlockList();
            nextBlockDataList.some(( nextBlock, index) => {
                if (nextBlock.getUUID() === this.getUUID()) {
                    nextBlockDataList.splice(index, 1);
                    return true;
                }
            });
        }

        /**  */
        var thisNextBlockDataList = this.getNextBlockList();
        var stack = [];
        
        if (thisNextBlockDataList.length !== 0) {
            stack.push(thisNextBlockDataList);
        }


        var iteration = 0;
        var current;
        while (stack.length !== 0) {
            /** FIXME: 무한루프 체크 */
            if (iteration > MAX_ITERATION) {
                console.log('무한루프');
                break;
            }
            
            current = stack.pop();
            /** 배열 일 때 */
            if (Array.isArray(current)) {
                current.forEach(element => {
                    stack.push(element);
                });
            } else {
                current.deleteBlock();
            }
        }
        if ( prevBlock ) {
            var type = prevBlock.getType();
            if (type === BLOCK_CODE_TYPE.CLASS || type === BLOCK_CODE_TYPE.DEF || type === BLOCK_CODE_TYPE.IF ||
                type === BLOCK_CODE_TYPE.FOR || type === BLOCK_CODE_TYPE.WHILE || type === BLOCK_CODE_TYPE.TRY
                || type === BLOCK_CODE_TYPE.ELSE || type === BLOCK_CODE_TYPE.ELIF || type === BLOCK_CODE_TYPE.FOR_ELSE 
                || type === BLOCK_CODE_TYPE.EXCEPT || type === BLOCK_CODE_TYPE.FINALLY) {

                var nullBlock = mapTypeToBlock(blockContainerThis, BLOCK_CODE_TYPE.NULL, {pointX: 0, pointY: 0});
                prevBlock.setNullBlock(nullBlock);
                prevBlock.appendBlock(nullBlock, BLOCK_DIRECTION.INDENT);
        
                $(prevBlock.getRootBlock().getContainerDom()).append(prevBlock.getNullBlock().getMainDom());
                $(prevBlock.getRootBlock().getContainerDom()).append(prevBlock.getHolderBlock().getMainDom());
            }
        }
        /** containerDom 삭제 */
        var containerDom = this.getContainerDom();
        $(containerDom).remove();
        $(containerDom).empty();

        /** blockContainer에서 block 데이터 삭제 제거 */
        var blockUuid = this.getUUID(); 
        blockContainerThis.deleteBlock(blockUuid);

        this.reRender();
        blockContainerThis.renderBlockLeftHolderListHeight();
    }

    Block.prototype.deleteBlockOne = function() {
            
        /** 렌더링된 rootDomElement 삭제 제거 */
        /** 부모 에서 this를 제거  */
        var prevBlock = this.getPrevBlock();
        
        if ( prevBlock ) {
            var nextBlockDataList = prevBlock.getNextBlockList();
            nextBlockDataList.some(( nextBlockBlock, index) => {
                if (nextBlockBlock.getUUID() === this.getUUID()) {
                    nextBlockDataList.splice(index, 1)
                    return true;
                }
            });
        }
        
        /**  */

        var thisNextBlockList = this.getNextBlockList();
        thisNextBlockList.forEach((block,index) => {
            if (block.getDirection() === this.getDirection()) {
                if (prevBlock) {
                    block.setPrevBlock(prevBlock);
                    prevBlock.appendBlock(block, block.getDirection());
                    prevBlock = block;
                }
            } else {
                if (prevBlock) {
                    block.setPrevBlock(prevBlock);
                    prevBlock.appendBlock(block, block.getDirection());
                    prevBlock = block;
                }
            }   
        });
        
        this.setNextBlockList([]);
        var mainDom = this.getMainDom();
        $(mainDom).remove();
        $(mainDom).empty();

        /** containerDom 삭제 */
        var containerDom = this.getContainerDom();
        $(containerDom).remove();
        $(containerDom).empty();

        /** blockContainer에서 block 데이터 삭제 제거 */
        var blockUuid = this.getUUID(); 
        var blockContainerThis = this.getBlockContainerThis();
        blockContainerThis.deleteBlock(blockUuid);
    }



    // ** --------------------------- Block dom 관련 메소드들 --------------------------- */

    Block.prototype.getMainDom = function() {
        return this.rootDom;
    }
    Block.prototype.setMainDom = function(rootDom) {
        this.rootDom = rootDom;
    }
    Block.prototype.getContainerDom = function() {
        return this.containerDom;
    }
    Block.prototype.setContainerDom = function(containerDom) {
        this.containerDom = containerDom;
    }
    Block.prototype.setBlockLeftHolderDom = function(blockLeftHolderDom) {
        this.blockLeftHolderDom = blockLeftHolderDom;
    }
    Block.prototype.getBlockLeftHolderDom = function() {
        return this.blockLeftHolderDom;
    }

    Block.prototype.reArrangeChildBlockDomList = function(arrangedBlock, rootBlockChildBlockListExceptChildBlock, direction) {
        var rootBlock = this.getRootBlock();

        var blockList = [];
        if (rootBlockChildBlockListExceptChildBlock === undefined) {
            blockList = rootBlock.selectChildBlockList();
        } else {
            blockList = rootBlockChildBlockListExceptChildBlock;
        }

        if (arrangedBlock === undefined) {
            return;
        }
        
        var containerDom = rootBlock.getContainerDom();
        var childDomList = containerDom.childNodes;
        var shadowDom;

        // var shadowIndex = 0;
        childDomList.forEach(( childDom,index) => {
            if ( parseInt( $(childDom).attr(STR_DATA_NUM_ID) ) === -1) {
                shadowDom = childDom;
                return true;
            }
        });


        blockList.some((childBlock, index) => {
            if (childBlock.getUUID() === arrangedBlock.getUUID()) {
                if ( parseInt( $(childBlock.getMainDom().nextSibling).attr(STR_DATA_NUM_ID) )  === -1 ){
                    return true;
                }

                var indentPxNum = 0;
                var depth = parseInt( $(childBlock.getMainDom()).attr(STR_DATA_DEPTH_ID) );
                if (isNaN(depth)){

                } else {
                    while (depth-- !== 0) {
                        indentPxNum += INDENT_DEPTH_PX;
                    }
                }

                if (direction === BLOCK_DIRECTION.INDENT) {
                    indentPxNum += INDENT_DEPTH_PX;
                }
                $(shadowDom).css(STR_MARGIN_LEFT, `${indentPxNum}${STR_PX}`);
    
                var childBlockCodeType = childBlock.getType();

                if(childBlockCodeType === BLOCK_CODE_TYPE.CLASS || childBlockCodeType === BLOCK_CODE_TYPE.DEF || childBlockCodeType === BLOCK_CODE_TYPE.IF ||
                    childBlockCodeType === BLOCK_CODE_TYPE.FOR || childBlockCodeType === BLOCK_CODE_TYPE.WHILE || childBlockCodeType === BLOCK_CODE_TYPE.TRY ||
                    childBlockCodeType === BLOCK_CODE_TYPE.ELSE || childBlockCodeType === BLOCK_CODE_TYPE.ELIF || childBlockCodeType === BLOCK_CODE_TYPE.FOR_ELSE || 
                    childBlockCodeType === BLOCK_CODE_TYPE.EXCEPT || childBlockCodeType === BLOCK_CODE_TYPE.FINALLY) {
                    
                    if ( childBlock.getNullBlock() ) {
                        $(childBlock.getNullBlock().getMainDom()).css(STR_DISPLAY, STR_NONE); 
                    }
                
                } else {
                    blockList.forEach((block, index) => {
                        if ( block.getNullBlock() ) {
                            $(block.getNullBlock().getMainDom()).css(STR_DISPLAY, STR_BLOCK); 
                        }
                    });
                }
                containerDom.insertBefore(shadowDom, childBlock.getMainDom().nextSibling);
                return true;
            }
        });
    }

    Block.prototype.makeChildBlockDomList = function(enumData) {
        // var that = this;
        var selectChildBlockList = this.selectChildBlockList();
        
        var childBlockDomList = [];
        var rootDepth = 0;
        selectChildBlockList.forEach((block, index) => {

            var depth = 0;
            var currBlock = block;
            // var blockName = block.getName();
            var direction = block.getDirection();

            if (direction === BLOCK_DIRECTION.INDENT) {
                var prevBlock = currBlock;
                while (prevBlock.getPrevBlock() !== null) {
                    prevBlock = prevBlock.getPrevBlock();
                    if (prevBlock.getDirection() === BLOCK_DIRECTION.DOWN ) {
            
                    } else {
                        depth++;
                    }
                }
            } else {
                var prevBlock = currBlock;
                while (prevBlock.getPrevBlock() !== null) {
                    prevBlock = prevBlock.getPrevBlock();
                    if (prevBlock.getDirection() === BLOCK_DIRECTION.INDENT) {
                        depth++;
                    } else {
                
                    }
                }
            }

            /** depth 계산 */
            var _depth = depth;
            var indentPxNum = 0;
            while (_depth-- !== 0) {
                indentPxNum += INDENT_DEPTH_PX;
            }
            indentPxNum -= rootDepth * INDENT_DEPTH_PX;

            /** index 0은 건너뛴다 */
            if (index === 0) {
                rootDepth = depth;
                return;
            } else {
                var mainDom = $(`<div class="vp-block" 
                                    style="margin-top:5px; 
                                            margin-bottom:5px; 
                                            position: relative;">
                                </div>`);
                var mainInnerDom = renderMainInnerDom();
                var mainHeaderDom = renderMainHeaderDom(currBlock);

                $(mainInnerDom).append(mainHeaderDom);
                $(mainDom).append(mainInnerDom);
        
                var backColor = '';
                if (currBlock.getType() === BLOCK_CODE_TYPE.CLASS || currBlock.getType() === BLOCK_CODE_TYPE.DEF) {
                    backColor = `${COLOR_BLUE}`;
                    $(mainDom).addClass('vp-block-class-def');
                } else if (currBlock.getType() === BLOCK_CODE_TYPE.IF || currBlock.getType() === BLOCK_CODE_TYPE.FOR
                    || currBlock.getType() === BLOCK_CODE_TYPE.WHILE || currBlock.getType() === BLOCK_CODE_TYPE.TRY
                    || currBlock.getType() === BLOCK_CODE_TYPE.ELSE || currBlock.getType() === BLOCK_CODE_TYPE.ELIF
                    || currBlock.getType() === BLOCK_CODE_TYPE.FOR_ELSE || currBlock.getType() === BLOCK_CODE_TYPE.EXCEPT 
                    || currBlock.getType() === BLOCK_CODE_TYPE.FINALLY) {
                    backColor = `${COLOR_RED}`;
                    $(mainDom).addClass('vp-block-if');
                }

                mainDom = this.renderBlockLeftHolderDom(mainDom, BLOCK_TYPE.SHADOW_BLOCK, {currBlock, backColor});

                if (currBlock.getType() === BLOCK_CODE_TYPE.HOLDER) {
                    $(mainDom).addClass('vp-block-bottom-holder');
                    $(mainDom).css(STR_MARGIN_TOP, `0px`);
                    $(mainDom).css(STR_OPACITY,'10');
                    if (currBlock.getSupportingBlock().getType() === BLOCK_CODE_TYPE.CLASS
                        || currBlock.getSupportingBlock().getType() === BLOCK_CODE_TYPE.DEF) {
                        $(mainDom).css(STR_BACKGROUND_COLOR,`${COLOR_BLUE}`);
                    } else {
                        $(mainDom).css(STR_BACKGROUND_COLOR,`${COLOR_RED}`);
                    }
                }
                if (currBlock.getType() === BLOCK_CODE_TYPE.NULL) {
                    $(mainDom).addClass('vp-block-nullblock');
                    $(mainDom).css(STR_OPACITY,'0');
                }

                $(mainDom).css(STR_MARGIN_LEFT, `${indentPxNum}${STR_PX}`);
                childBlockDomList.push(mainDom);
            }
        });
        return childBlockDomList;
    }

    Block.prototype.getMainDomPosition = function() {
        var mainDom = this.getMainDom();
        var clientRect = $(mainDom)[0].getBoundingClientRect();
        return clientRect;
    }

    // ** --------------------------- Block 멤버변수의 set, get 관련 메소드들 --------------------------- */

    Block.prototype.setPointX = function(pointX) {
        this.setState({
            pointX
        });
    }
    Block.prototype.setPointY = function(pointY) {
        this.setState({
            pointY
        });
    }
    Block.prototype.getPointX = function() {
        return this.state.pointX;
    }
    Block.prototype.getPointY = function() {
        return this.state.pointY;
    }
    Block.prototype.setContainerPointX = function(containerPointX) {
        this.setState({
            containerPointX
        });
    }
    Block.prototype.setContainerPointY = function(containerPointY) {
        this.setState({
            containerPointY
        });
    }
    Block.prototype.getContainerPointX = function() {
        return this.state.containerPointX;
    }
    Block.prototype.getContainerPointY = function() {
        return this.state.containerPointY;
    }



    Block.prototype.getType = function() {
        return this.state.type;
    }
    Block.prototype.setType = function(type) {
        this.setState({
            type
        });
    }
    Block.prototype.getName = function() {
        return this.state.name;
    }
    Block.prototype.setName = function(name) {
        this.setState({
            name
        });
    }
    Block.prototype.getUUID = function() {
        return this.state.uuid;
    }
    Block.prototype.setDirection = function(direction) {
        this.setState({
            direction
        })
    }
    Block.prototype.getDirection = function() {
        return this.state.direction;
    }



    Block.prototype.getBlockContainerThis = function() {
        return this.blockContainerThis;
    }
    Block.prototype.renderBlockLeftHolderHeight = function(px) {
        $( this.getBlockLeftHolderDom() ).css(STR_HEIGHT,`${px}${STR_PX}`);
    }
    Block.prototype.resetBlockLeftHolderHeight = function() {
        $( this.getBlockLeftHolderDom() ).css(STR_HEIGHT,`42${STR_PX}`);
    }
    Block.prototype.getTempBlockLeftHolderHeight = function() {
        return this.state.tempBlockLeftHolderHeight;
    }
    Block.prototype.setTempBlockLeftHolderHeight = function(tempBlockLeftHolderHeight) {
        this.setState({
            tempBlockLeftHolderHeight
        })
    }


    // ** --------------------------- Block render 관련 메소드들 --------------------------- */

    Block.prototype.reRender = function() {
        
        var rootBlock = this.getRootBlock();
        var _containerDom = rootBlock.getContainerDom();
        $(_containerDom).empty();
        $(_containerDom).remove();

        var containerDom = document.createElement(STR_DIV);
        containerDom.classList.add(STR_CSS_CLASS_VP_BLOCK_CONTAINER);

        rootBlock.setContainerDom(containerDom);
        $(containerDom).css(STR_TOP,`${rootBlock.getContainerPointY()}` + STR_PX);
        $(containerDom).css(STR_LEFT,`${rootBlock.getContainerPointX()}` + STR_PX);

        var blockStackList = rootBlock.renderChildBlockListIndentAndGet();

        blockStackList.forEach((block, index) => {
            var mainDom = block.getMainDom();
            $(mainDom).css(STR_TOP,`${0}` + STR_PX);
            $(mainDom).css(STR_LEFT,`${0}` + STR_PX);
            $(mainDom).attr(STR_DATA_NUM_ID,`${index}`);
            $(containerDom).append(mainDom);
            block.bindEventAll();
        });

        $(STR_CSS_CLASS_VP_NODEEDITOR_LEFT).append(containerDom);
    }

    Block.prototype.renderMyColor = function() {
        var type = this.getType();
        if (type === BLOCK_CODE_TYPE.HOLDER || type === BLOCK_CODE_TYPE.NULL) {
            return;
        }

        if (type === BLOCK_CODE_TYPE.CLASS || type === BLOCK_CODE_TYPE.DEF) {
            $(this.getMainDom()).css(STR_BACKGROUND_COLOR, `${COLOR_BLUE}`);
            $(this.getMainDom()).find(STR_CSS_CLASS_VP_BLOCK_LEFT_HOLDER).css(STR_BACKGROUND_COLOR, `${COLOR_BLUE}`);
            $(this.getHolderBlock().getMainDom()).css(STR_BACKGROUND_COLOR, `${COLOR_BLUE}`);
        } else if (type === BLOCK_CODE_TYPE.IF || type === BLOCK_CODE_TYPE.FOR
            || type === BLOCK_CODE_TYPE.WHILE || type === BLOCK_CODE_TYPE.TRY
            || type === BLOCK_CODE_TYPE.ELSE || type === BLOCK_CODE_TYPE.ELIF
            || type === BLOCK_CODE_TYPE.FOR_ELSE || type === BLOCK_CODE_TYPE.EXCEPT || type === BLOCK_CODE_TYPE.FINALLY) {
            $(this.getMainDom()).css(STR_BACKGROUND_COLOR, `${COLOR_RED}`);
            $(this.getMainDom()).find(STR_CSS_CLASS_VP_BLOCK_LEFT_HOLDER).css(STR_BACKGROUND_COLOR, `${COLOR_RED}`);
            $(this.getHolderBlock().getMainDom()).css(STR_BACKGROUND_COLOR, `${COLOR_RED}`);
        } else {
            $(this.getMainDom()).css(STR_BACKGROUND_COLOR, `${COLOR_GREEN}`); 
            $(this.getMainDom()).find(STR_CSS_CLASS_VP_BLOCK_LEFT_HOLDER).css(STR_BACKGROUND_COLOR, `${COLOR_GREEN}`);
        }
    }

    Block.prototype.renderResetColor = function() {
        var that = this;
        var blockContainerThis = that.getBlockContainerThis();
        var blockList = blockContainerThis.getBlockList();
        blockList.forEach(block => {
            var type = block.getType();

            $(block.getMainDom()).css(STR_BORDER, '2px solid transparent');
            $(block.getMainDom()).find(STR_CSS_CLASS_VP_BLOCK_LEFT_HOLDER).css('box-shadow','0');
    
            if (that.getHolderBlock()) {
                $(that.getHolderBlock().getMainDom()).css('box-shadow','0');
                $(that.getHolderBlock().getMainDom()).css(STR_BORDER,'2px solid transparent');
            }
            
            if (type === BLOCK_CODE_TYPE.CLASS || type === BLOCK_CODE_TYPE.DEF) {
                $(block.getMainDom()).css(STR_BACKGROUND_COLOR, COLOR_BLUE);
                $(block.getMainDom()).find(STR_CSS_CLASS_VP_BLOCK_LEFT_HOLDER).css(STR_BACKGROUND_COLOR, COLOR_BLUE);
                $(block.getHolderBlock().getMainDom()).css(STR_BACKGROUND_COLOR, COLOR_BLUE);
            } else if (type === BLOCK_CODE_TYPE.IF || type === BLOCK_CODE_TYPE.FOR
                || type === BLOCK_CODE_TYPE.WHILE || type === BLOCK_CODE_TYPE.TRY
                || type === BLOCK_CODE_TYPE.ELSE || type === BLOCK_CODE_TYPE.ELIF 
                || type === BLOCK_CODE_TYPE.FOR_ELSE || type === BLOCK_CODE_TYPE.EXCEPT || type === BLOCK_CODE_TYPE.FINALLY) {
                $(block.getMainDom()).css(STR_BACKGROUND_COLOR, COLOR_RED);
                $(block.getMainDom()).find(STR_CSS_CLASS_VP_BLOCK_LEFT_HOLDER).css(STR_BACKGROUND_COLOR, COLOR_RED);
                $(block.getHolderBlock().getMainDom()).css(STR_BACKGROUND_COLOR, COLOR_RED);
            } else {
                $(block.getMainDom()).css(STR_BACKGROUND_COLOR, COLOR_GREEN); 
                $(block.getMainDom()).find(STR_CSS_CLASS_VP_BLOCK_LEFT_HOLDER).css(STR_BACKGROUND_COLOR, COLOR_GREEN);
            }
        });
        var blockList = blockContainerThis.getBlockList();
        blockList.forEach(block => {
            var mainDom = block.getMainDom();
            $(mainDom).find(STR_CSS_CLASS_VP_BLOCK_DELETE_BTN).remove();
        });
    }

    Block.prototype.renderChildBlockListIndentAndGet = function() {
        var selectChildBlockList = this.selectChildBlockList();
        var rootDepth = 0;

        selectChildBlockList.forEach((block, index) => {
            var depth = 0;
            var currBlock = block;
            // var blockName = block.getName();
            var direction = block.getDirection();

            if (direction === BLOCK_DIRECTION.INDENT) {
                var prevBlock = currBlock;
                while (prevBlock.getPrevBlock() !== null) {
                    prevBlock = prevBlock.getPrevBlock();
                    if (prevBlock.getDirection() === BLOCK_DIRECTION.DOWN ) {
            
                    } else {
                        depth++;
                    }
                }
            } 
            else {
                var prevBlock = currBlock;
                while (prevBlock.getPrevBlock() !== null) {
                    prevBlock = prevBlock.getPrevBlock();
                    if (prevBlock.getDirection() === BLOCK_DIRECTION.INDENT) {
                        depth++;
                    } else {
                
                    }
                }
            }

            /** depth 계산 */
            var _depth = depth;
            var indentPxNum = 0;
            while (_depth-- !== 0) {
                indentPxNum += INDENT_DEPTH_PX;
            }
    
            indentPxNum -= rootDepth * INDENT_DEPTH_PX;
            /** index 0일때 rootDepth를 계산*/
            if (index === 0) {
                rootDepth = depth;
                return;
            }

            var rootDom = block.getMainDom();

            $(rootDom).css(STR_MARGIN_LEFT, `${indentPxNum}${STR_PX}`);
            $(rootDom).attr(STR_DATA_DEPTH_ID, depth);
            var rect = block.getMainDomPosition();
            block.setPointX(rect.x);
            block.setPointY(rect.y);
            var x = block.getPointX();
            var y = block.getPointY();

            $(rootDom).css(STR_TOP,`${y}` + STR_PX);
            $(rootDom).css(STR_LEFT,`${x}` + STR_PX);

        });
        return selectChildBlockList;
    }

    Block.prototype.renderBlockLeftHolderDom = function(mainDom, blockType , optionData) {
        var blockCodeType = this.getType();
        if (blockType === BLOCK_TYPE.BLOCK) {
            if (blockCodeType === BLOCK_CODE_TYPE.CLASS || blockCodeType === BLOCK_CODE_TYPE.DEF) {
                $(mainDom).addClass('vp-block-class-def');
            }

            if (blockCodeType === BLOCK_CODE_TYPE.IF || blockCodeType === BLOCK_CODE_TYPE.FOR
                || blockCodeType === BLOCK_CODE_TYPE.WHILE || blockCodeType === BLOCK_CODE_TYPE.TRY
                || blockCodeType === BLOCK_CODE_TYPE.ELSE || blockCodeType === BLOCK_CODE_TYPE.ELIF
                || blockCodeType === BLOCK_CODE_TYPE.FOR_ELSE || blockCodeType  === BLOCK_CODE_TYPE.EXCEPT 
                || blockCodeType === BLOCK_CODE_TYPE.FINALLY) {
                $(mainDom).addClass('vp-block-if');
            }

            if (blockCodeType === BLOCK_CODE_TYPE.CLASS || blockCodeType === BLOCK_CODE_TYPE.DEF || blockCodeType === BLOCK_CODE_TYPE.IF ||
                blockCodeType === BLOCK_CODE_TYPE.FOR || blockCodeType === BLOCK_CODE_TYPE.WHILE || blockCodeType === BLOCK_CODE_TYPE.TRY || 
                blockCodeType === BLOCK_CODE_TYPE.ELSE || blockCodeType === BLOCK_CODE_TYPE.ELIF || blockCodeType === BLOCK_CODE_TYPE.FOR_ELSE || 
                blockCodeType === BLOCK_CODE_TYPE.EXCEPT || blockCodeType === BLOCK_CODE_TYPE.FINALLY) {
                var blockLeftHolderDom = $('<div class="vp-block-left-holder"></div>');
                this.setBlockLeftHolderDom(blockLeftHolderDom);
                $(mainDom).append(blockLeftHolderDom);
            }
        
        } else if (blockType === BLOCK_TYPE.MOVE_BLOCK){

            if (blockCodeType === BLOCK_CODE_TYPE.CLASS 
                || blockCodeType === BLOCK_CODE_TYPE.DEF) {
                var blockLeftHolderDom = $('<div class="vp-block-left-holder"></div>');
                var blockLeftHolderHeight = this.getTempBlockLeftHolderHeight();
                blockLeftHolderDom.css(STR_HEIGHT,`${blockLeftHolderHeight}px`);
        
                $(mainDom).append(blockLeftHolderDom);
                $(mainDom).addClass('vp-block-class-def');
            }  
        
            if (blockCodeType === BLOCK_CODE_TYPE.IF || blockCodeType === BLOCK_CODE_TYPE.FOR
                || blockCodeType === BLOCK_CODE_TYPE.WHILE || blockCodeType === BLOCK_CODE_TYPE.TRY
                || blockCodeType === BLOCK_CODE_TYPE.ELSE || blockCodeType === BLOCK_CODE_TYPE.ELIF
                || blockCodeType === BLOCK_CODE_TYPE.FOR_ELSE || blockCodeType === BLOCK_CODE_TYPE.EXCEPT 
                || blockCodeType === BLOCK_CODE_TYPE.FINALLY) {
                var blockLeftHolderDom = $('<div class="vp-block-left-holder"></div>');
                var blockLeftHolderHeight = this.getTempBlockLeftHolderHeight();
                blockLeftHolderDom.css(STR_HEIGHT,`${blockLeftHolderHeight}px`);
        
                $(mainDom).append(blockLeftHolderDom);
                $(mainDom).addClass('vp-block-if');
            }
        } else {
            const {currBlock, backColor} = optionData;
            if (currBlock.getType() === BLOCK_CODE_TYPE.CLASS || currBlock.getType() === BLOCK_CODE_TYPE.DEF) {
                var blockLeftHolderDom = $('<div class="vp-block-left-holder"></div>');
                var blockLeftHolderHeight = currBlock.getTempBlockLeftHolderHeight();
                blockLeftHolderDom.css(STR_HEIGHT,`${blockLeftHolderHeight}px`);

                $(mainDom).addClass('vp-block-class-def');
                $(blockLeftHolderDom).css(STR_BACKGROUND_COLOR,`${backColor}`);
                $(mainDom).append(blockLeftHolderDom);
            }         

            if (currBlock.getType() === BLOCK_CODE_TYPE.IF || currBlock.getType() === BLOCK_CODE_TYPE.FOR
                || currBlock.getType() === BLOCK_CODE_TYPE.WHILE || currBlock.getType() === BLOCK_CODE_TYPE.TRY
                || currBlock.getType() === BLOCK_CODE_TYPE.ELSE || currBlock.getType() === BLOCK_CODE_TYPE.ELIF
                || currBlock.getType() === BLOCK_CODE_TYPE.FOR_ELSE || currBlock.getType() === BLOCK_CODE_TYPE.EXCEPT 
                || currBlock.getType() === BLOCK_CODE_TYPE.FINALLY) {
                var blockLeftHolderDom = $('<div class="vp-block-left-holder"></div>');
                var blockLeftHolderHeight = currBlock.getTempBlockLeftHolderHeight();
                blockLeftHolderDom.css(STR_HEIGHT,`${blockLeftHolderHeight}px`);
    
                $(mainDom).addClass('vp-block-if');
                $(blockLeftHolderDom).css(STR_BACKGROUND_COLOR,`${backColor}`);
                $(mainDom).append(blockLeftHolderDom);
            }
        }
        return mainDom;
    }

    Block.prototype.renderBottomOption = function() {
        var that = this;
        var name = that.getName();

        $('.vp-nodeeditor-tab-navigation-node-option-title span').html(`${name.charAt(0).toUpperCase() + name.slice(1)} Option`);
        $(STR_CSS_CLASS_VP_NODEEDITOR_BOTTOM_TAB_VIEW).empty();
        
        var type = that.getType();
        switch(type) {
            /** class */
            case BLOCK_CODE_TYPE.CLASS: {
                var classContainer = renderBottomOptionContainer();
                var classBlockOption = renderBottomOptionContainerInner();
                /** class name */
                var classInnerDom = renderBottomOptionInnerDom();
                var classNameState = that.getState(STATE_className);                                
                var classNameDom = renderBottomOptionName(classNameState, BLOCK_CODE_TYPE.CLASS);
                classInnerDom.append( classNameDom );
                classBlockOption.append(classInnerDom);

                /** class parameter list */
                var classInParamList = that.getState(STATE_classInParamList);
                var classInParamContainer = renderInParamContainer(classInParamList, BLOCK_CODE_TYPE.CLASS);

                // classInParam 갯수만큼 bottom block 옵션에 렌더링
                var classInParamBody = $(`<div class='vp-nodeeditor-body'>
                                        </div>`);

                classInParamList.forEach((classInParam, index ) => {
                    // console.log('defInParam', defInParam);
                    var classInParamDom = renderInParamDom(classInParam, index, BLOCK_CODE_TYPE.CLASS);
                    var deleteButton = $(`<button class='vp-block-btn'>x</button>`);
                    $(deleteButton).click(function() {
                        that.setState({
                            classInParamList:  [ ...that.getState(STATE_classInParamList).slice(0, index), 
                                                ...that.getState(STATE_classInParamList).slice(index+1, that.getState(STATE_classInParamList).length) ]
                        });

                        var classInParamStr = `(`;
                        that.getState(STATE_classInParamList).forEach((classInParam, index ) => {
                            classInParamStr += `${classInParam}`;
                            if (that.getState(STATE_classInParamList).length - 1 !== index ) {
                                classInParamStr += `, `;
                            }
                        });
                        classInParamStr += `) : `;
                        $(`.vp-block-header-class-param-${that.getUUID()}`).html(classInParamStr);
                        that.renderBottomOption();
                    });
                    classInParamDom.append(deleteButton);
                    classInParamBody.append(classInParamDom);
                });
                classInParamContainer.append(classInParamBody);
                classBlockOption.append(classInParamContainer);

            


                /** */
                classContainer.append(classBlockOption);

                /** option 탭에 렌더링된 dom객체 생성 */
                $(STR_CSS_CLASS_VP_NODEEDITOR_BOTTOM_TAB_VIEW).append(classContainer);

                /** class 파라미터 변경 이벤트 함수 바인딩 */
                classInParamList.forEach((classInParam, index ) => {
                    $(`.vp-nodeeditor-input-class-inparam-${index}`).on(STR_CHANGE_KEYUP_PASTE, function() {
                        var newParam = $(this).val();
                        // console.log('newParam', newParam);
                        that.setState({
                            classInParamList:  [ ...that.getState(STATE_classInParamList).slice(0, index), newParam,
                                                ...that.getState(STATE_classInParamList).slice(index+1, that.getState(STATE_classInParamList).length) ]
                        });
                        var classInParamStr = generateClassInParamList(that);
                        $(`.vp-block-header-class-param-${that.getUUID()}`).html(classInParamStr);
                    });
                });

                /** 함수 파라미터 생성 이벤트 함수 바인딩 */
                $(`.vp-nodeeditor-class-inparam-plus-btn`).click(function() {
                    // console.log('def in param plus');
                    var newData = '';
                    that.setState({
                        classInParamList: [ ...that.getState(STATE_classInParamList), newData ]
                    });
                    that.renderBottomOption();
                });

                /** class 이름 변경 함수 바인딩 */
                $(`.vp-nodeeditor-input-class-name`).on(STR_CHANGE_KEYUP_PASTE, function() {
                    that.setState({
                        className: $(this).val()
                    });

                    $(`.vp-block-header-class-name-${that.getUUID()}`).html($(this).val());
                });

                break;
            }
            /** def */
            case BLOCK_CODE_TYPE.DEF: {
                var defContainer = renderBottomOptionContainer();
                var defBlockOption = renderBottomOptionContainerInner();
                
                /** 함수 이름 function name */
                var defInnerDom = renderBottomOptionInnerDom();
                var defName = that.getState(STATE_defName);
                var defNameDom = renderBottomOptionName(defName, BLOCK_CODE_TYPE.DEF);

                defInnerDom.append( defNameDom );
                defBlockOption.append(defInnerDom);

                /** 함수 파라미터 */
                var defInParamList = that.getState(STATE_defInParamList);
                var defInParamContainer = renderInParamContainer(defInParamList, BLOCK_CODE_TYPE.DEF);

                // defInParam 갯수만큼 bottom block 옵션에 렌더링
                var defInParamBody = $(`<div class='vp-nodeeditor-elifbody'>
                                        </div>`);

                defInParamList.forEach((defInaPram, index ) => {
                    var defInParamDom = renderInParamDom(defInaPram, index, BLOCK_CODE_TYPE.DEF);
                    var deleteButton = $(`<button class='vp-block-btn'>x</button>`);
                    $(deleteButton).click(function() {
                        that.setState({
                            defInParamList:  [ ...that.getState(STATE_defInParamList).slice(0, index), 
                                                ...that.getState(STATE_defInParamList).slice(index+1, that.getState(STATE_defInParamList).length) ]
                        });

                        var defInParamStr = generateDefInParamList(that);
                        $(`.vp-block-header-def-param-${that.getUUID()}`).html(defInParamStr);
                        that.renderBottomOption();
                    });
                    defInParamDom.append(deleteButton);
                    defInParamBody.append(defInParamDom);
                });
                defInParamContainer.append(defInParamBody);
                defBlockOption.append(defInParamContainer);
                /** */
                defContainer.append(defBlockOption);

                /** bottom block option 탭에 렌더링된 dom객체 생성 */
                $(STR_CSS_CLASS_VP_NODEEDITOR_BOTTOM_TAB_VIEW).append(defContainer);

                /** 함수 파라미터 변경 이벤트 함수 바인딩 */
                defInParamList.forEach((defInParam, index ) => {
                    $(`.vp-nodeeditor-input-def-inparam-${index}`).on(STR_CHANGE_KEYUP_PASTE, function() {
                        var newParam = $(this).val();
                        that.setState({
                            defInParamList:  [ ...that.getState(STATE_defInParamList).slice(0, index), newParam,
                                                ...that.getState(STATE_defInParamList).slice(index+1, that.getState(STATE_defInParamList).length) ]
                        });
                        var defInParamStr = generateDefInParamList(that);
                        $(`.vp-block-header-def-param-${that.getUUID()}`).html(defInParamStr);
                    });
                });

                /** 함수 파라미터 생성 이벤트 함수 바인딩 */
                $(`.vp-nodeeditor-def-inparam-plus-btn`).click(function() {
                    var newData = '';
                    that.setState({
                        defInParamList: [ ...that.getState(STATE_defInParamList), newData ]
                    });
                    that.renderBottomOption();
                });

                /** 함수 이름 변경 */
                $(`.vp-nodeeditor-input-def-name`).on(STR_CHANGE_KEYUP_PASTE, function() {
                    that.setState({
                        defName: $(this).val()
                    });
                    $(`.vp-block-header-def-name-${that.getUUID()}`).html($(this).val());
                });

                break;
            }
            /** if */
            case BLOCK_CODE_TYPE.IF: {
                var uuid = that.getUUID();
                var bottomOptionContainer = renderBottomOptionContainer();
                var ifBlockOption  = renderBottomOptionContainerInner();
                var defaultOrDetailButton = renderDefaultOrDetailButton(uuid);

                /* --------------------------- if ----------------------------- */
                var ifTitle = renderBottomOptionTitle(STR_IF);
                var ifNameDom = renderBottomOptionName(that.getState(STATE_ifCodeLine), BLOCK_CODE_TYPE.IF);
                
                ifBlockOption.append(defaultOrDetailButton);
                ifTitle.append(ifNameDom);
                ifBlockOption.append(ifTitle);

                /* --------------------------- elif ---------------------------* */
                var elifList = [];
                var nextBlockDataList = that.getNextBlockList();
                var stack = [];
                if (nextBlockDataList.length !== 0) {
                    stack.push(nextBlockDataList);
                }

                var isBreak = false;
                var current;
                while (stack.length !== 0) {
                    current = stack.shift();
                    /** 배열 일 때 */
                    if (Array.isArray(current)) {
                        current.forEach(element => {
                            if ( element.getDirection() === BLOCK_DIRECTION.DOWN 
                                && element.getType() === BLOCK_CODE_TYPE.IF) {
                                isBreak = true;
                            }

                            if (element.getDirection() === BLOCK_DIRECTION.DOWN ) {
                                stack.push(element);
                                if ( element.getType() === BLOCK_CODE_TYPE.ELIF) {
                                    elifList.push(element);
                                }
                            }
                        });
                    
        
                    } else {
                        var currBlock = current;
                        var nextBlockDataList = currBlock.getNextBlockList();
                        stack.unshift(nextBlockDataList);
                    }

                    if (isBreak) {
                        break;
                    }
                }


                var elifContainer = $(`<div class='vp-nodeeditor-option-container'
                                            style='margin-top:5px;'>
                                            <div class='vp-nodeeditor-tab-navigation-node-block-title'>
                                                <span class='vp-block-optiontab-name'>elif</span>
                                                <div class='vp-nodeeditor-style-flex-row-center' >
                                                    <span class='vp-nodeeditor-elif-number'
                                                        style='margin-right:5px;'>
                                                        ${elifList.length} Block
                                                    </span>
                                                    <button class='vp-block-btn vp-nodeeditor-elif-plus-btn'
                                                            style='margin-right:5px;'>
                                                        + elif
                                                    </button>
                                                    <div class='vp-nodeeditor-option-vertical-btn'>▼</div>
                                                </div>
                                            </div>
                                        </div>`);

                // elif 갯수만큼 bottom block 옵션에 렌더링
                var elifBody = $(`<div class='vp-nodeeditor-elifbody'>
                                </div>`);

                elifList.forEach((elifData, index ) => {
                    var elifDom = renderInParamDom(elifData.getState(STATE_elifCodeLine), index, BLOCK_CODE_TYPE.ELIF, elifData.getUUID());
                    var deleteButton = $(`<button class='vp-block-btn'>x</button>`);
                    $(deleteButton).click(function() {
                        /** 부모 에서 this를 제거  */
                        var prevBlock = elifData.getPrevBlock();
                        if ( prevBlock ) {
                            var nextBlockDataList = prevBlock.getNextBlockList();
                            nextBlockDataList.some(( nextBlock, index) => {
                                if (nextBlock.getUUID() === elifData.getUUID()) {
                                    nextBlockDataList.splice(index, 1);
                                    return true;
                                }
                            });
                        }

                        elifData.setPrevBlock(null);
                        elifData.getNullBlock().deleteBlockOne();
                        elifData.getHolderBlock().deleteBlockOne();

                        $(elifData.getMainDom()).remove();
                        $(elifData.getContainerDom()).remove();

                        that.renderBottomOption();
                        
                        var blockContainerThis = that.getBlockContainerThis();
                        blockContainerThis.renderBlockLeftHolderListHeight();

                        blockContainerThis.deleteBlock(elifData.getUUID());
                    });
                    elifDom.append(deleteButton);
                    elifBody.append(elifDom);
                });
                elifContainer.append(elifBody);
                ifBlockOption.append(elifContainer);

                /* ---------------------------------- else ------------------------------------- */
                var elseBlock= renderElseBlock(that, BLOCK_CODE_TYPE.IF);
                ifBlockOption.append(elseBlock);
                bottomOptionContainer.append(ifBlockOption);

                /** bottom block option 탭에 렌더링된 dom객체 생성 */
                $(STR_CSS_CLASS_VP_NODEEDITOR_BOTTOM_TAB_VIEW).append(bottomOptionContainer);

                /** --------------------------------- if Option 이벤트 함수 바인딩 ---------------------------------- */
                /** if code 변경 */
                $(`.vp-nodeeditor-if-input`).on(STR_CHANGE_KEYUP_PASTE, function() {
                    that.setState({
                        ifCodeLine: $(this).val()
                    });
                    $(`.vp-block-header-if-code-${that.getUUID()}`).html(that.getState(STATE_ifCodeLine));
                });

                var uuid = that.getUUID();
                /** else yes */
                $(`.vp-nodeeditor-else-yes-${uuid}`).click(function() {
                    that.setState({
                        isIfElse: true
                    });
                    that.renderBottomOption();
                });

                /** else no */
                $(`.vp-nodeeditor-else-no-${uuid}`).click(function() {
                    that.setState({
                        isIfElse: false
                    });
                    that.renderBottomOption();
                });

                // /** default 옵션 클릭 */
                // $(`.vp-nodeeditor-default-option-${uuid}`).click(function() {
                //     if ( $(this).hasClass('vp-nodeeditor-option-btn-selected') === true) {
                //         $(this).removeClass('vp-nodeeditor-option-btn-selected');
                //         $(`.vp-nodeeditor-detail-option-${uuid}`).addClass('vp-nodeeditor-option-btn-selected');
                //     } else {
                //         $(this).addClass('vp-nodeeditor-option-btn-selected');
                //         $(`.vp-nodeeditor-detail-option-${uuid}`).removeClass('vp-nodeeditor-option-btn-selected');
                //     }
                // });
                // /** detail 옵션 클릭 */
                // $(`.vp-nodeeditor-detail-option-${uuid}`).click(function() {
                //     if ( $(this).hasClass('vp-nodeeditor-option-btn-selected') === true) {
                //         $(this).removeClass('vp-nodeeditor-option-btn-selected');
                //         $(`.vp-nodeeditor-default-option-${uuid}`).addClass('vp-nodeeditor-option-btn-selected');
                //     } else {
                //         $(this).addClass('vp-nodeeditor-option-btn-selected');
                //         $(`.vp-nodeeditor-default-option-${uuid}`).removeClass('vp-nodeeditor-option-btn-selected');
                //     }
                // });

                /** elif 생성 이벤트 함수 바인딩 */
                $(`.vp-nodeeditor-elif-plus-btn`).click(function() {
                    var elifCodeLine = '';
                    that.setState({
                        elifList: [ ...that.getState(STATE_elifList), elifCodeLine ]
                    });
                    /** ++ elif */
                    var blockContainerThis = that.getBlockContainerThis();
                    var newBlock = mapTypeToBlock(blockContainerThis, BLOCK_CODE_TYPE.ELIF, {pointX: 0, pointY: 0})

                    that.getHolderBlock().appendBlock(newBlock, BLOCK_DIRECTION.DOWN);
                    that.renderBottomOption();

                    blockContainerThis.renderBlockLeftHolderListHeight();
                });

                /** elif code 변경 */
                elifList.forEach((elifData, index) => {
                    $(`.vp-nodeeditor-elif-input-${elifData.getUUID()}`).on(STR_CHANGE_KEYUP_PASTE, function() {
                        var updatedData = $(this).val();
                        elifData.setState({
                            elifCodeLine: updatedData
                        });
                        $(`.vp-block-header-elif-code-${elifData.getUUID()}`).html(updatedData);
                    });
                });
                break;
            }  
            case BLOCK_CODE_TYPE.ELIF: {
                var uuid = that.getUUID();
                var bottomOptionContainer = renderBottomOptionContainer();
                var elifBlockOption  = renderBottomOptionContainerInner();
                var elifContainer = renderBottomOptionTitle(STR_ELIF);
                var elifNameDom = renderBottomOptionName(that.getState(STATE_elifCodeLine), BLOCK_CODE_TYPE.ELIF, uuid);

                // elifBlockOption.append(ifButton);
                elifContainer.append(elifNameDom);
                elifBlockOption.append(elifContainer);

                bottomOptionContainer.append(elifBlockOption);

                /** bottom block option 탭에 렌더링된 dom객체 생성 */
                $(STR_CSS_CLASS_VP_NODEEDITOR_BOTTOM_TAB_VIEW).append(bottomOptionContainer);

                $(`.vp-nodeeditor-elif-input-${uuid}`).on(STR_CHANGE_KEYUP_PASTE, function() {
                    var updatedData = $(this).val();
                    that.setState({
                        elifCodeLine: updatedData
                    });
                    $(`.vp-block-header-elif-code-${uuid}`).html(updatedData);
                });
                break;
            }     
            /** for */
            case BLOCK_CODE_TYPE.FOR: {
                var bottomOptionContainer = renderBottomOptionContainer();
                var forBlockOption = renderBottomOptionContainerInner();

                /* ------------- for -------------- */
                var forContainer = renderBottomOptionTitle(STR_FOR);
                var forNameDom = renderBottomOptionName(that.getState(STATE_forCodeLine), BLOCK_CODE_TYPE.FOR);

                forContainer.append(forNameDom);
                forBlockOption.append(forContainer);
                /* ------------- else ------------- */
                var elseBlock = renderElseBlock(that, BLOCK_CODE_TYPE.FOR);
                forBlockOption.append(elseBlock);
                bottomOptionContainer.append(forBlockOption);

                /** bottom block option 탭에 렌더링된 dom객체 생성 */
                $(STR_CSS_CLASS_VP_NODEEDITOR_BOTTOM_TAB_VIEW).append(bottomOptionContainer);

                /** for code 변경 */
                $(`.vp-nodeeditor-for-input`).on(STR_CHANGE_KEYUP_PASTE, function() {
                    that.setState({
                        forCodeLine: $(this).val()
                    });
                    $(`.vp-block-header-for-code-${that.getUUID()}`).html(that.getState(STATE_forCodeLine));
                });

                var uuid = that.getUUID();
                $(`.vp-nodeeditor-else-yes-${uuid}`).click(function() {
                    that.setState({
                        isForElse: true
                    });
                    that.renderBottomOption();
                });

                $(`.vp-nodeeditor-else-no-${uuid}`).click(function() {
                    that.setState({
                        isForElse: false
                    });
                    that.renderBottomOption();
                });
                break;
            }
            /** while */
            case BLOCK_CODE_TYPE.WHILE: {
                var flexRow = renderBottomOptionContainer();
                var whileBlockOption = renderBottomOptionContainerInner();

                /* ------------- while -------------- */
                var whileContainer = renderBottomOptionTitle('while');
                var whileDom = renderBottomOptionName(that.getState(STATE_whileCodeLine), BLOCK_CODE_TYPE.WHILE);

                whileContainer.append(whileDom );
                whileBlockOption.append(whileContainer);
                flexRow.append(whileBlockOption);

                /** bottom block option 탭에 렌더링된 dom객체 생성 */
                $(STR_CSS_CLASS_VP_NODEEDITOR_BOTTOM_TAB_VIEW).append(flexRow);

                /** if code 변경 */
                $(`.vp-nodeeditor-while-input`).on(STR_CHANGE_KEYUP_PASTE, function() {
                    that.setState({
                        whileCodeLine: $(this).val()
                    });
                    $(`.vp-block-header-while-code-${that.getUUID()}`).html(that.getState(STATE_whileCodeLine));
                });
                break;
            }
            /** import */
            case BLOCK_CODE_TYPE.IMPORT: {
                var baseImportList = that.getState('baseImportList');

                var flexRow = renderBottomOptionContainer();
                var importBlockOption = renderBottomOptionContainerInner();
                /* ------------- import -------------- */
                var countisImport = 0;
                baseImportList.forEach(baseImportData => {
                    if (baseImportData.isImport === true ) {
                        countisImport += 1;
                    };
                });
                var defaultImportContainer = $(`<div class='vp-nodeeditor-blockoption-default-import-container'>
                                                    <div class='vp-nodeeditor-tab-navigation-node-block-title'>
                                                        <span class='vp-block-optiontab-name'>default</span>
                                                        <div class='vp-nodeeditor-style-flex-row-center'>
                                                            <span class='vp-nodeeditor-default-import-number'
                                                                    style='margin-right:5px;'>
                                                                ${countisImport} Selected
                                                            </span>
                                                            <div class='vp-nodeeditor-option-vertical-btn'>▼</div>
                                                        </div>
                                                    </div>
                                                </div>`);
                var defaultImportBody = $('<div><div>');
                baseImportList.forEach((baseImportData,index) => {
                    const { isImport, baseImportName, baseAcronyms } = baseImportData;

                    var defaultImportDom = $(`<div class='vp-nodeeditor-style-flex-row-between'
                                                    style='padding: 0.1rem 0;'>
                                                    <div class='vp-nodeeditor-style-flex-column-center'>
                                                        <input class='vp-nodeeditor-blockoption-default-import-input-${index}' 
                                                                type='checkbox' 
                                                                ${isImport === true ? 'checked': ''}>
                                                        </input>
                                                    </div>
                                                    <div class='vp-nodeeditor-style-flex-column-center'>
                                                        <span style='font-size:12px; font-weight:700;'> ${baseImportName}</span>
                                                    </div>
                                                    <div class='vp-nodeeditor-style-flex-column-center'
                                                        style='width: 50%;     text-align: center;'>
                                                        <span class=''>${baseAcronyms}</span>
                                            
                                                    </div>
                                            </div>`);
                    defaultImportBody.append(defaultImportDom);                        
                });
                defaultImportContainer.append(defaultImportBody);
                importBlockOption.append(defaultImportContainer);

                /** -------------custom import ------------------ */
                var customImportList = that.getState(STATE_customImportList);
                var countIsCustomImport = 0;
                customImportList.forEach(baseImportData => {
                    if (baseImportData.isImport === true ) {
                        countIsCustomImport += 1;
                    };
                });
                // customImport 갯수만큼 bottom block 옵션에 렌더링
                var customImportContainer = $(`<div class='vp-nodeeditor-blockoption-custom-import-container'>
                                                    <div class='vp-nodeeditor-tab-navigation-node-block-title'>
                                                        <span class='vp-block-optiontab-name'>custom</span>
                                                        <div class='vp-nodeeditor-style-flex-row-center'>

                                                            <span class='vp-nodeeditor-elif-number'
                                                                    style='margin-right:5px;'>
                                                                ${countIsCustomImport} Selected
                                                            </span>
                                                            <button class='vp-block-btn vp-nodeeditor-custom-import-plus-btn'
                                                                    style='margin-right:5px;'>
                                                                + import
                                                            </button>
                                                            <div class='vp-nodeeditor-option-vertical-btn'>▼</div>
                                                        </div>
                                                    </div>
                                                </div>`);

                var customImportBody = $(`<div class='vp-nodeeditor-customimport-body'>
                                        </div>`);
                customImportList.forEach((customImportData, index ) => {
                    const { isImport, baseImportName, baseAcronyms } = customImportData;
                
                    var customImportDom = $(`<div class='vp-nodeeditor-style-flex-row-between'>
                                                    <div class='vp-nodeeditor-style-flex-column-center'>
                                                        <input class='vp-nodeeditor-blockoption-custom-import-input
                                                                    vp-nodeeditor-blockoption-custom-import-input-${index}' 
                                                                type='checkbox' 
                                                                ${isImport === true ? 'checked': ''}>
                                                        </input>
                                                    </div>
                                                    <select class='vp-nodeeditor-select
                                                                    vp-nodeeditor-blockoption-custom-import-select
                                                                    vp-nodeeditor-blockoption-custom-import-select-${index}'
                                                            style='margin-right:5px;'>
                                                        <option value='numpy' ${baseImportName === 'numpy' ? STR_SELECTED: ''}>
                                                            numpy
                                                        </option>
                                                        <option value='pandas' ${baseImportName === 'pandas' ? STR_SELECTED: ''}>
                                                            pandas
                                                        </option>
                                                        <option value='matplotlib' ${baseImportName === 'matplotlib' ? STR_SELECTED: ''}>
                                                            matplotlib
                                                        </option>
                                                        <option value='seaborn' ${baseImportName === 'seaborn' ? STR_SELECTED: ''}>
                                                            seaborn
                                                        </option>
                                                        <option value='os' ${baseImportName === 'os' ? STR_SELECTED: ''}>
                                                            os
                                                        </option>
                                                        <option value='pandas' ${baseImportName === 'sys' ? STR_SELECTED: ''}>
                                                            sys
                                                        </option>
                                                        <option value='time' ${baseImportName === 'time' ? STR_SELECTED: ''}>
                                                            time
                                                        </option>
                                                        <option value='datetime' ${baseImportName === 'datetime' ? STR_SELECTED: ''}>
                                                            datetime
                                                        </option>
                                                        <option value='random' ${baseImportName === 'random' ? STR_SELECTED: ''}>
                                                            random
                                                        </option>
                                                        <option value='math' ${baseImportName === 'math' ? STR_SELECTED: ''}>
                                                            math
                                                        </option>
                                                    </select>
                                                    <div class='vp-nodeeditor-style-flex-column-center'>
                                                        <input class='vp-nodeeditor-blockoption-custom-import-textinput
                                                                    vp-nodeeditor-blockoption-custom-import-textinput-${index}'
                                                                style='' 
                                                                type='text' 
                                                                placeholder='input import'
                                                                value='${baseAcronyms}'></input>
                                                    </div>
                                            </div>`);
                    var deleteButton = $(`<button class='vp-block-btn'
                                                style='margin-top: 5px;'>x</button>`);
                    $(deleteButton).click(function() {
                        that.setState({
                            customImportList:  [ ...that.getState(STATE_customImportList).slice(0, index), 
                                                ...that.getState(STATE_customImportList).slice(index+1, that.getState(STATE_customImportList).length) ]
                        });
                        that.renderBottomOption();
                    });
                    customImportDom.append(deleteButton);
                    customImportBody.append(customImportDom);
                });
                customImportContainer.append(customImportBody);
                importBlockOption.append(customImportContainer);

                flexRow.append(importBlockOption);
            
                $(STR_CSS_CLASS_VP_NODEEDITOR_BOTTOM_TAB_VIEW).append(flexRow);

                $('.vp-nodeeditor-custom-import-plus-btn').click(function() {
                    var newData = {
                        baseAcronyms : ''
                        , baseImportName : 'numpy'
                        , isImport : false
                    }
                    that.setState({
                        customImportList: [ ...that.getState(STATE_customImportList), newData ]
                    });
                    that.renderBottomOption();
                });

                customImportList.forEach((customImportData, index) => {
                    const { isImport, baseImportName, baseAcronyms } = customImportData;
                    $(`.vp-nodeeditor-blockoption-custom-import-input-${index}`).click(function() {
                        if (isImport === true) {
                            var updatedData = {
                                baseAcronyms: that.getState(STATE_customImportList)[index].baseAcronyms
                                , baseImportName
                                , isImport: false
                            }
                            that.setState({
                                customImportList: [ ...that.getState(STATE_customImportList).slice(0, index), updatedData
                                                    , ...that.getState(STATE_customImportList).slice(index+1, that.getState(STATE_customImportList).length) ]
                            });
                        } else {
                            var updatedData = {
                                baseAcronyms
                                , baseImportName
                                , isImport: true
                            }
                            that.setState({
                                customImportList: [ ...that.getState(STATE_customImportList).slice(0, index), updatedData
                                                    , ...that.getState(STATE_customImportList).slice(index+1, that.getState(STATE_customImportList).length) ]
                            });
                        }
                        that.renderBottomOption();
                    })
                    $(`.vp-nodeeditor-blockoption-custom-import-select-${index}`).change(function()  {
                        var updatedData = {
                            baseAcronyms: that.getState(STATE_customImportList)[index].baseAcronyms
                            , baseImportName : $(STR_COLON_SELECTED, this).val()
                            , isImport
                        }
                        that.setState({
                            customImportList: [ ...that.getState(STATE_customImportList).slice(0, index), updatedData
                                                , ...that.getState(STATE_customImportList).slice(index+1, that.getState(STATE_customImportList).length) ]
                        });
                        that.renderBottomOption();
                    });
                    $(`.vp-nodeeditor-blockoption-custom-import-textinput-${index}`).on(STR_CHANGE_KEYUP_PASTE, function() {
                        var updatedData = {
                            baseAcronyms : $(this).val()
                            , baseImportName 
                            , isImport
                        }
                        that.setState({
                            customImportList: [ ...that.getState(STATE_customImportList).slice(0, index), updatedData
                                                , ...that.getState(STATE_customImportList).slice(index+1, that.getState(STATE_customImportList).length) ]
                        });

                    });
                });
                
                baseImportList.forEach((_, index) => {
                    $(`.vp-nodeeditor-blockoption-default-import-input-${index}`).click(function() {

                        var isImport = that.getState(STATE_baseImportList)[index].isImport;
                        var baseImportName = that.getState(STATE_baseImportList)[index].baseImportName;
                        var baseAcronyms = that.getState(STATE_baseImportList)[index].baseAcronyms;

                        if (isImport === true) {
                            var updatedData = {
                                isImport: false
                                , baseImportName
                                , baseAcronyms
                            }
                    
                            that.setState({
                                baseImportList: [ ...that.getState(STATE_baseImportList).slice(0, index), updatedData
                                                , ...that.getState(STATE_baseImportList).slice(index+1, that.getState(STATE_baseImportList).length) ]
                            });
                        } 
                        else  {
                            var updatedData = {
                                isImport: true
                                , baseImportName
                                , baseAcronyms
                                
                            }
                        
                            that.setState({
                                baseImportList: [ ...that.getState(STATE_baseImportList).slice(0, index), updatedData
                                                , ...that.getState(STATE_baseImportList).slice(index+1, that.getState(STATE_baseImportList).length) ]
                            });
                        }
                        that.renderBottomOption();
                    }); 
                });
                break;
            }
            /** api */
            case BLOCK_CODE_TYPE.API: {
                var apiContainer = renderBottomOptionContainer();
                var apiBlockOption  = renderBottomOptionContainerInner();
                /* ---------------- Api --------------- */
                var apiTitle = renderBottomOptionTitle('navigator'); 

                var apiDom = $(`<div class="vp-nodeeditor-tab-navigation-node-body
                                            vp-nodeeditor-tab-navigation-node-block-body
                                            vp-nodeeditor-style-flex-row-between-wrap">
                                            <div class="vp-nodeeditor-tab-navigation-node-block-body-btn">
                                                <span>NUMPY</span>
                                            </div>
                                            <div class="vp-nodeeditor-tab-navigation-node-block-body-btn">
                                                <span>PANDAS</span>
                                            </div>
                                            <div class="vp-nodeeditor-tab-navigation-node-block-body-btn">
                                                <span>OS</span>
                                            </div>
                                            <div class="vp-nodeeditor-tab-navigation-node-block-body-btn">
                                                <span>SYS</span>
                                            </div>
                                            <div class="vp-nodeeditor-tab-navigation-node-block-body-btn">
                                                <span>DATE</span>
                                            </div>
                                            <div class="vp-nodeeditor-tab-navigation-node-block-body-btn">
                                                <span>DATETIME</span>
                                            </div>
                                            <div class="vp-nodeeditor-tab-navigation-node-block-body-btn">
                                                <span>MATH</span>
                                            </div>
                                            <div class="vp-nodeeditor-tab-navigation-node-block-body-btn">
                                                <span>RANDOM</span>
                                            </div>
                                        </div>`);
                apiTitle.append(apiDom);
                apiBlockOption.append(apiTitle);                      
                apiContainer.append(apiBlockOption);
                /** bottom block option 탭에 렌더링된 dom객체 생성 */
                $(STR_CSS_CLASS_VP_NODEEDITOR_BOTTOM_TAB_VIEW).append(apiContainer);
                break;
            }

            /** try */
            case BLOCK_CODE_TYPE.TRY: {
                var blockOptionContainer = renderBottomOptionContainer();
                var tryBlockOption  = renderBottomOptionContainerInner();

                /* ---------------- Try --------------- */
                var tryTitle = renderBottomOptionTitle('try');
                tryBlockOption.append(tryTitle);

                /* ---------------- except ------------- */
                var exceptList = [];
                var nextBlockDataList = that.getNextBlockList();
                var stack = [];
                if (nextBlockDataList.length !== 0) {
                    stack.push(nextBlockDataList);
                }

                var current;
                while (stack.length !== 0) {
                    current = stack.shift();
                    /** 배열 일 때 */
                    if (Array.isArray(current)) {
                        current.forEach(element => {
                            if (element.getDirection() === BLOCK_DIRECTION.DOWN) {
                            
                                stack.push(element);
                                if ( element.getType() === BLOCK_CODE_TYPE.EXCEPT) {
                                    exceptList.push(element);
                                }
                            }
                        });
                    
        
                    } else {
                        var currBlock = current;
                        var nextBlockDataList = currBlock.getNextBlockList();
                        stack.unshift(nextBlockDataList);
                    }
                }


                var exceptContainer = $(`<div class='vp-nodeeditor-option-container'>
                                            <div class='vp-nodeeditor-tab-navigation-node-block-title'>
                                                <span class='vp-block-optiontab-name'>except</span>
                                                <div class='vp-nodeeditor-style-flex-row-center' >
                                                    <span class='vp-nodeeditor-elif-number'
                                                        style='margin-right:5px;'>
                                                        ${exceptList.length} Block
                                                    </span>
                                                    <button class='vp-block-btn vp-nodeeditor-except-plus-btn'
                                                            style='margin-right:5px;'>
                                                        + except
                                                    </button>
                                                    <div class='vp-nodeeditor-option-vertical-btn'>▼</div>
                                                </div>
                                            </div>
                                        </div>`);

                // except 갯수만큼 bottom block 옵션에 렌더링
                var exceptBody = $(`<div class='vp-nodeeditor-elifbody'>
                                    </div>`);

                exceptList.forEach((exceptData, index ) => {
                    var exceptDom = renderInParamDom(exceptData.getState(STATE_exceptCodeLine), index, BLOCK_CODE_TYPE.EXCEPT);
                    var deleteButton = $(`<button class='vp-block-btn'>x</button>`);
                    $(deleteButton).click(function() {
            
                        // /** 부모 에서 this를 제거  */
                        var prevBlock = exceptData.getPrevBlock();
                        if ( prevBlock ) {
                            var nextBlockDataList = prevBlock.getNextBlockList();
                            nextBlockDataList.some(( nextBlock, index) => {
                                if (nextBlock.getUUID() === exceptData.getUUID()) {
                                    nextBlockDataList.splice(index, 1);
                                    return true;
                                }
                            });
                        }

                        exceptData.setPrevBlock(null);
                        exceptData.getNullBlock().deleteBlockOne();
                        exceptData.getHolderBlock().deleteBlockOne();

                        $(exceptData.getMainDom()).remove();
                        $(exceptData.getContainerDom()).remove();

                        that.renderBottomOption();

                        var blockContainerThis = that.getBlockContainerThis();
                        blockContainerThis.renderBlockLeftHolderListHeight();

                        blockContainerThis.deleteBlock(exceptData.getUUID());
                    });
                    exceptDom.append(deleteButton);
                    exceptBody.append(exceptDom);
                });
                exceptContainer.append(exceptBody);
                tryBlockOption.append(exceptContainer);

                /* ---------------- Finally ----------- */
                var finallyContainer = $(`<div class='vp-nodeeditor-option-container'>
                                            <div class='vp-nodeeditor-tab-navigation-node-block-title'>
                                                <span class='vp-block-optiontab-name'>finally</span>
                                                <div class='vp-nodeeditor-style-flex-row-center'>
                                                    <select class='vp-nodeeditor-blockoption-finally-select'
                                                            style='margin-right:5px;'>
                                                        <option value='no' ${this.getState(STATE_isFinally) === false 
                                                                            ? STR_SELECTED: ''}>No</option>
                                                        <option value='${STR_YES}' ${this.getState(STATE_isFinally) === true 
                                                                            ? STR_SELECTED: ''}>Yes</option>
                                                    </select>
                                                    <div class='vp-nodeeditor-option-vertical-btn'>▼</div>
                                                </div>
                                            </div>
                                        </div>`);

                tryBlockOption.append(finallyContainer);

                blockOptionContainer.append(tryBlockOption);
                /** bottom block option 탭에 렌더링된 dom객체 생성 */
                $(STR_CSS_CLASS_VP_NODEEDITOR_BOTTOM_TAB_VIEW).append(blockOptionContainer);


                /** except 생성 이벤트 함수 바인딩 */
                $(`.vp-nodeeditor-except-plus-btn`).click(function() {
                    var exceptCodeLine = '';
                    that.setState({
                        exceptList: [ ...that.getState(STATE_exceptList), exceptCodeLine ]
                    });

                    /** ++ except */
                    var blockContainerThis = that.getBlockContainerThis();
                    var newBlock = mapTypeToBlock(blockContainerThis, BLOCK_CODE_TYPE.EXCEPT, {pointX: 0, pointY: 0})
                        
                    that.getHolderBlock().appendBlock(newBlock, BLOCK_DIRECTION.DOWN);
                
                    that.renderBottomOption();
                    that.reRender();
                    var blockContainerThis = that.getBlockContainerThis();
                    blockContainerThis.renderBlockLeftHolderListHeight();
                });

                /** except code 변경 */
                exceptList.forEach((exceptData, index ) => {
                    $(`.vp-nodeeditor-except-input-${index}`).on(STR_CHANGE_KEYUP_PASTE, function() {
                        var updatedData = $(this).val();
                        exceptData.setState({
                            exceptCodeLine: updatedData
                        });
                        $(`.vp-block-header-except-code-${exceptData.getUUID()}`).html(updatedData);
                    });
                });

                /** finally select 이벤트 함수 바인딩 */
                $('.vp-nodeeditor-blockoption-finally-select').change(function() {
                    var isFinally = $(STR_COLON_SELECTED, this).val();
                    if (isFinally === STR_YES) {
                        /** else 생성 */
                        var nextBlockDataList = that.getNextBlockList();
                        var stack = [];
                        if (nextBlockDataList.length !== 0) {

                        }
                
                    } else {
                    /** else 삭제 */
                
                    }

                    that.reRender();
                    var blockContainerThis = that.getBlockContainerThis();
                    blockContainerThis.renderBlockLeftHolderListHeight();
                });
                break;
            }

            /** return */
            case BLOCK_CODE_TYPE.RETURN: {
                var blockOptionContainer = renderBottomOptionContainer();
                var returnBlockOption  = renderBottomOptionContainerInner();

                var returnOutParamList = that.getState(STATE_returnOutParamList);
                var returnOutParamContainer = renderInParamContainer(returnOutParamList, BLOCK_CODE_TYPE.RETURN);

                // defInParam 갯수만큼 bottom block 옵션에 렌더링
                var returnOutParamBody = $(`<div class='vp-nodeeditor-returnbody'>
                                            </div>`);

                returnOutParamList.forEach((returnOutParam, index ) => {
                    var returnOutParamDom = renderInParamDom(returnOutParam, index, BLOCK_CODE_TYPE.RETURN);
    
                    var deleteButton = $(`<button class='vp-block-btn'>x</button>`);
                    $(deleteButton).click(function() {
                        that.setState({
                            returnOutParamList:  [ ...that.getState(STATE_returnOutParamList).slice(0, index), 
                                                    ...that.getState(STATE_returnOutParamList).slice(index+1, that.getState(STATE_returnOutParamList).length) ]
                        });

                        var returnOutParamStr = ` `;
                        that.getState(STATE_returnOutParamList).forEach((returnOutParam, index ) => {
                            returnOutParamStr += `${returnOutParam}`;
                            if (that.getState(STATE_returnOutParamList).length - 1 !== index ) {
                                returnOutParamStr += `, `;
                            }
                        });
                        returnOutParamStr += ``;
                        $(`.vp-block-header-return-param-${that.getUUID()}`).html(returnOutParamStr);

                        that.renderBottomOption();
                    });
                    returnOutParamDom.append(deleteButton);
                    returnOutParamBody.append(returnOutParamDom);
                });
                returnOutParamContainer.append(returnOutParamBody);
                returnBlockOption.append(returnOutParamContainer);

                /** */
                blockOptionContainer.append(returnBlockOption);

                /** bottom block option 탭에 렌더링된 dom객체 생성 */
                $(STR_CSS_CLASS_VP_NODEEDITOR_BOTTOM_TAB_VIEW).append(blockOptionContainer);

                /** 함수 파라미터 변경 이벤트 함수 바인딩 */
                returnOutParamList.forEach((_, index ) => {
                    $(`.vp-nodeeditor-return-outparam-${index}`).on(STR_CHANGE_KEYUP_PASTE, function() {
                        var newParam = $(this).val();
                        that.setState({
                            returnOutParamList:  [ ...that.getState(STATE_returnOutParamList).slice(0, index), newParam,
                                                    ...that.getState(STATE_returnOutParamList).slice(index+1, that.getState(STATE_returnOutParamList).length) ]
                        });
                        var returnOutParamStr = ` `;
                        that.getState(STATE_returnOutParamList).forEach((returnOutParam, index ) => {
                            returnOutParamStr += `${returnOutParam}`;
                            if (that.getState(STATE_returnOutParamList).length - 1 !== index ) {
                                returnOutParamStr += `, `;
                            }
                        });
                        returnOutParamStr += ``;
                        $(`.vp-block-header-return-param-${that.getUUID()}`).html(returnOutParamStr);
                    });
                });

                /** 함수 파라미터 생성 이벤트 함수 바인딩 */
                $(`.vp-nodeeditor-return-outparam-plus-btn`).click(function() {
                    // console.log('def in param plus');
                    var newData = '';
                    that.setState({
                        returnOutParamList: [ ...that.getState(STATE_returnOutParamList), newData ]
                    });
                    that.renderBottomOption();
                });

                break;
            }
            case BLOCK_CODE_TYPE.CODE: {
                var blockOptionContainer = renderBottomOptionContainer();
                var blockOptionInner = renderBottomOptionContainerInner();

                /* ------------- code -------------- */
                var codeDomContainer = renderBottomOptionTitle('code');
                var codeDom = renderBottomOptionName(that.getState(STATE_customCodeLine), BLOCK_CODE_TYPE.CODE);

                codeDomContainer.append(codeDom );
                blockOptionInner.append(codeDomContainer);
                blockOptionContainer.append(blockOptionInner);
                /** bottom block option 탭에 렌더링된 dom객체 생성 */
                $(STR_CSS_CLASS_VP_NODEEDITOR_BOTTOM_TAB_VIEW).append(blockOptionContainer);

                /** code 변경 */
                $(`.vp-nodeeditor-code-input`).on(STR_CHANGE_KEYUP_PASTE, function() {
                    that.setState({
                        customCodeLine: $(this).val()
                    });
                    $(`.vp-block-header-custom-code-${that.getUUID()}`).html(that.getState(STATE_customCodeLine));
                });
                break;
            }
        }
        $('.vp-nodeeditor-option-vertical-btn').click(function() {
            if ($(this).hasClass(STR_CSS_CLASS_VP_NODEEDITOR_ARROW_DOWN)) {
                $(this).removeClass(STR_CSS_CLASS_VP_NODEEDITOR_ARROW_DOWN);
                $(this).addClass(STR_CSS_CLASS_VP_NODEEDITOR_ARROW_UP);
                $(this).html(`▲`);
                $(this).parent().parent().parent().removeClass(STR_CSS_CLASS_VP_NODEEDITOR_MINIMIZE);
            } else {
                $(this).removeClass(STR_CSS_CLASS_VP_NODEEDITOR_ARROW_UP);
                $(this).addClass(STR_CSS_CLASS_VP_NODEEDITOR_ARROW_DOWN);
                $(this).html(`▼`);
                $(this).parent().parent().parent().addClass(STR_CSS_CLASS_VP_NODEEDITOR_MINIMIZE);
            }
        });
    }

    // ** --------------------------- Block state 관련 메소드들 --------------------------- */
    Block.prototype.setState = function(newState) {
        this.state = changeOldToNewState(this.state, newState);
        this.consoleState();
    }

    /**특정 state Name 값을 가져오는 함수
        @param {string} stateKeyName
    */
    Block.prototype.getState = function(stateKeyName) {
        return findStateValue(this.state, stateKeyName);
    }
    Block.prototype.getStateAll = function() {
        return this.state;
    }
    Block.prototype.consoleState = function() {
        // console.log(this.state);
    }



    /** ---------------------------이벤트 함수 바인딩--------------------------- */
    Block.prototype.bindEventAll = function() {
        if (this.getType() === BLOCK_CODE_TYPE.HOLDER || this.getType() === BLOCK_CODE_TYPE.EXCEPT
            || this.getType() === BLOCK_CODE_TYPE.FOR_ELSE || this.getType() === BLOCK_CODE_TYPE.FINALLY) {

        } else if (this.getType() === BLOCK_CODE_TYPE.ELSE || this.getType() === BLOCK_CODE_TYPE.ELIF) {
            this.bindClickEvent();
        } else {
            this.bindDragEvent();
            this.bindClickEvent();
        }
    }

    Block.prototype.bindDragEvent = function() {
        var that = this;
        var blockContainerThis = this.getBlockContainerThis();
        var blockCodeType = this.getType();

        var oldMainDom = this.getMainDom();
        var x = 0;
        var y = 0;
        var pos1 = 0;
        var pos2 = 0;
        var pos3 = 0;
        var pos4 = 0;
        var pointX = this.getPointX();
        var pointY = this.getPointY();

        var newMainDom;
        var tempChildListDom;

        var shadowBlock;
        var shadowBlockList = [];
        var rootBlockChildBlockListExceptChildBlock = [];
        var selectedBlock = null;
        var selectedBlockDirection = null;

        var thisBlockHeightPx = 0;
        var isParentCollicion = false;
        var beforeBlockList = [];


        // .vp-nodeeditor-right

        $(oldMainDom).draggable({ 
            revert: 'invalid',
            revertDuration: 200,
            appendTo: STR_CSS_CLASS_VP_NODEEDITOR_LEFT,
            cursor: 'move', 
            start: (event, ui) => {
                newMainDom = document.createElement(STR_DIV);
                newMainDom.classList.add('vp-block');
                $(newMainDom).css(STR_POSITION, STR_ABSOLUTE);

                var mainInnerDom = $(`<div class='vp-block-inner'></div>`);
                var nameDom = renderMainHeaderDom(this);

                //FIXME:
                tempChildListDom = $(`<div class='vp-block-stack'><div>`);
                var childBlockDomList = that.makeChildBlockDomList(MAKE_CHILD_BLOCK.MOVE);
                childBlockDomList.forEach(childDom => {
                    tempChildListDom.append(childDom);
                });
                $(mainInnerDom).append(nameDom);
                $(newMainDom).append(mainInnerDom);
                $(newMainDom).append(tempChildListDom);

                newMainDom = that.renderBlockLeftHolderDom(newMainDom, BLOCK_TYPE.MOVE_BLOCK);

                $(STR_CSS_CLASS_VP_NODEEDITOR_LEFT).append(newMainDom);

                ({ beforeBlockList, afterBlockList } = that.splitBlockList());

                var childBlockList = that.selectChildBlockList();
                childBlockList.forEach(block => {
                    var mainDom = block.getMainDom();
                    $(mainDom).css(STR_OPACITY, '0');
                    thisBlockHeightPx += BLOCK_HEIGHT_PX;
                });

                var rootBlockList = blockContainerThis.getRootBlockList();
                rootBlockList.forEach((rootBlock, index) => {
                    var shadowChildBlockDomList = that.makeChildBlockDomList(MAKE_CHILD_BLOCK.SHADOW);
                    shadowBlock = new ShadowBlock(blockContainerThis, blockCodeType, {pointX: 0, pointY: 0}, shadowChildBlockDomList,  BLOCK_TYPE.BLOCK, that);
                    shadowBlock.setRootBlockUUID(rootBlock.getUUID());
                    shadowBlockList.push(shadowBlock);

                    var containerDom = rootBlock.getContainerDom();
                    $(shadowBlock.getMainDom()).css(STR_DISPLAY,STR_NONE);
                    $(shadowBlock.getMainDom()).removeClass(STR_CSS_CLASS_VP_SELECTED_SHADOWBLOCK);
                    $(containerDom).append(shadowBlock.getMainDom());
                });

                that.setShadowBlock(shadowBlockList);
                blockContainerThis.renderBlockLeftHolderListHeight();
            },
            drag:(event, ui) => {
                blockContainerThis.renderBlockLeftHolderListHeight();
                var rect = that.getMainDomPosition();
                
                that.setPointX(rect.x);
                that.setPointY(rect.y);

                buttonX = event.clientX; 
                buttonY = event.clientY; 

                pos1 = pos3 - buttonX;
                pos2 = pos4 - buttonY;
                pos3 = buttonX;
                pos4 = buttonY;

                x = buttonX - pos2 - $(STR_CSS_CLASS_VP_NODEEDITOR_LEFT).offset().left  - rect.width / 2;
                y = buttonY - pos1 - $(STR_CSS_CLASS_VP_NODEEDITOR_LEFT).offset().top;
                $(newMainDom).css(STR_TOP,`${y}` + STR_PX);
                $(newMainDom).css(STR_LEFT,`${x }` + STR_PX);
                var blockList = blockContainerThis.getBlockList();
                var { x: thisX, y: thisY, 
                    width: thisBlockWidth, height: thisBlockHeight} = that.getMainDomPosition();
                buttonX = thisX; 
                buttonY = thisY; 

                blockList.forEach(block => {
                    if (that.getUUID() === block.getUUID()) {
                        return;
                    }
                    var blockCodeType = block.getType();
                    var { x, y, 
                        width: blockWidth, height: blockHeight} = block.getMainDomPosition();
                    var rootBlock = block.getRootBlock();
                    var rootBlockChildBlockList = rootBlock.selectChildBlockList();
                    var childBlockList = that.selectChildBlockList();
                    rootBlockChildBlockList.forEach((rootBlockChildBlock) => {
                        var is = childBlockList.some((childBlock) => {
                            if ( rootBlockChildBlock.getUUID() === childBlock.getUUID() ) {
                                return true;
                            } 
                        });

                        if (is) {
            
                        } else {
                            rootBlockChildBlockListExceptChildBlock.push(rootBlockChildBlock);
                        }
                    });

                    var is = shadowBlockList.some(shadowBlock => {
                        if ( $(shadowBlock.getMainDom()).hasClass(STR_CSS_CLASS_VP_SELECTED_SHADOWBLOCK) ) {
                            return true;
                        }
                    });
                    if (is === false) {
                        $(oldMainDom).css('transform', `translate(0px, 0px)`); 
                    }

                    /** 블럭 충돌 로직 */
                    if ( x < buttonX
                        && buttonX < (x + blockWidth + blockWidth)
                        && y  < buttonY
                        && buttonY < (y + blockHeight) ) {     
                        if (block.getType() === BLOCK_CODE_TYPE.NULL) {
                            return;
                        }
                        var rootBlockList = blockContainerThis.getRootBlockList();
                        isParentCollicion = beforeBlockList.some((beforeBlock,index) => {
                            if (beforeBlock.getUUID() === block.getUUID()) {
                                $(oldMainDom).css('transform', `translate(0px, -${thisBlockHeightPx}px)`); 
                                return true;
                            }
                        });

                        if (isParentCollicion === false) {
                            $(oldMainDom).css('transform', `translate(0px, 0px)`); 
                        }

                        shadowBlockList.some(shadowBlock => {
                            if (shadowBlock.getRootBlockUUID() === rootBlock.getUUID()) {
                                var isChild = childBlockList.some(childBlock => {
                                    if (childBlock.getUUID() === block.getUUID()) {
                                        return true;
                                    }
                                });
                                if (isChild === true) {
                                    return true;
                                }

                                /** 내가 이동한 블럭이 루트 블럭일 경우 쉐도우 블록을 생성하지 않는다 */
                                if (that.getUUID() !== rootBlock.getUUID() ) {
                                                                    
                                    // console.log(STR_BLOCK, block.getName());
                                    $(shadowBlock.getMainDom()).css(STR_DISPLAY,STR_BLOCK);
                                    $(shadowBlock.getMainDom()).addClass(STR_CSS_CLASS_VP_SELECTED_SHADOWBLOCK);
                                    shadowBlock.setSelectBlock(block);
                                
                                    if (blockCodeType === BLOCK_CODE_TYPE.CLASS || blockCodeType === BLOCK_CODE_TYPE.DEF || blockCodeType === BLOCK_CODE_TYPE.IF ||
                                        blockCodeType === BLOCK_CODE_TYPE.FOR || blockCodeType === BLOCK_CODE_TYPE.WHILE || blockCodeType === BLOCK_CODE_TYPE.TRY ||
                                        blockCodeType === BLOCK_CODE_TYPE.ELSE || blockCodeType === BLOCK_CODE_TYPE.ELIF || blockCodeType === BLOCK_CODE_TYPE.FOR_ELSE || 
                                        blockCodeType === BLOCK_CODE_TYPE.EXCEPT || blockCodeType === BLOCK_CODE_TYPE.FINALLY) {

                                        var is = block.getNextBlockList().some(nextBlock => {
                                            if ( nextBlock.getType() === BLOCK_CODE_TYPE.NULL ) {
                                            
                                                // var holderBlock = block.getHolderBlock();
                                                var blockLeftHolderHeight = block.getTempBlockLeftHolderHeight();
                                                block.getBlockLeftHolderDom().css(STR_HEIGHT,`${blockLeftHolderHeight}px`);
                                                // $(holderBlock.getMainDom()).css('transform', `translate(0px, -34px)`); 

                                                return true;
                                            }
                                        });
                                    }

                                    if (blockCodeType === BLOCK_CODE_TYPE.HOLDER) {
                                        $(block.getMainDom()).css('transform', `translate(0px, 0px)`); 
                                    }
                                }

                                return true;
                            }
                        });
                        // var type = block.getType();
                        if (blockCodeType === BLOCK_CODE_TYPE.CLASS || blockCodeType === BLOCK_CODE_TYPE.DEF || blockCodeType === BLOCK_CODE_TYPE.IF ||
                            blockCodeType === BLOCK_CODE_TYPE.FOR || blockCodeType === BLOCK_CODE_TYPE.WHILE || blockCodeType === BLOCK_CODE_TYPE.TRY ||
                            blockCodeType === BLOCK_CODE_TYPE.ELSE || blockCodeType === BLOCK_CODE_TYPE.ELIF || blockCodeType === BLOCK_CODE_TYPE.FOR_ELSE || 
                            blockCodeType === BLOCK_CODE_TYPE.EXCEPT || blockCodeType === BLOCK_CODE_TYPE.FINALLY) {
                            selectedBlockDirection = BLOCK_DIRECTION.INDENT;
                        } else if (blockCodeType === BLOCK_CODE_TYPE.HOLDER) {
                            selectedBlockDirection = BLOCK_DIRECTION.DOWN; 
                        } else {
                            selectedBlockDirection = BLOCK_DIRECTION.DOWN; 
                        }
                        rootBlock.reArrangeChildBlockDomList(block, rootBlockChildBlockListExceptChildBlock, selectedBlockDirection);
                    } else {
                        var blockCodeType = block.getType();
                        if (blockCodeType === BLOCK_CODE_TYPE.HOLDER) {
                            $(block.getMainDom()).css('transform', `translate(0px, 0px)`); 
                        }
                        // var type = block.getType();
                        if (blockCodeType === BLOCK_CODE_TYPE.CLASS || blockCodeType === BLOCK_CODE_TYPE.DEF || blockCodeType === BLOCK_CODE_TYPE.IF ||
                            blockCodeType === BLOCK_CODE_TYPE.FOR || blockCodeType === BLOCK_CODE_TYPE.WHILE || blockCodeType === BLOCK_CODE_TYPE.TRY ||
                            blockCodeType === BLOCK_CODE_TYPE.ELSE || blockCodeType === BLOCK_CODE_TYPE.ELIF || blockCodeType === BLOCK_CODE_TYPE.FOR_ELSE || 
                            blockCodeType === BLOCK_CODE_TYPE.EXCEPT || blockCodeType === BLOCK_CODE_TYPE.FINALLY) {
                            var is = shadowBlockList.some(shadowBlock => {
                                if ( $(shadowBlock.getMainDom()).hasClass(STR_CSS_CLASS_VP_SELECTED_SHADOWBLOCK) ) {
                                    selectedBlock = shadowBlock.getSelectBlock();
                                    return true;
                                }
                            });
                        }
            
                        var rootBlockList = that.getRootBlockList();
                
                        rootBlockList.some(_rootBlock => {
                            var containerDom = _rootBlock.getContainerDom();
                            var containerDomRect = $(containerDom)[0].getBoundingClientRect();
                            var { x, y, width: containerDomWidth, height: containerDomHeight} = containerDomRect;
            
                            if ( x < event.clientX
                                && event.clientX < (x + containerDomWidth)
                                && y  < event.clientY
                                && event.clientY < (y + containerDomHeight) ) {  
                                // console.log('in colision');
                            } else {
                                shadowBlockList.forEach(shadowBlock => {
                                    if (shadowBlock.getRootBlockUUID() === _rootBlock.getUUID()) {
                                        $(shadowBlock.getMainDom()).css(STR_DISPLAY,STR_NONE);
                                        $(shadowBlock.getMainDom()).removeClass(STR_CSS_CLASS_VP_SELECTED_SHADOWBLOCK);
                                        shadowBlock.setSelectBlock(null);
                                    }    
                                });
                                // console.log('not colision');
                            }
                        });
                    }
                    rootBlockChildBlockListExceptChildBlock = [];
                });
            }, 
            stop: function(event, ui) {
                // 화면 밖으로 나갔을 때, 재조정
                var maxHeight = $(STR_CSS_CLASS_VP_NODEEDITOR_LEFT).height();
                var maxWidth = $(STR_CSS_CLASS_VP_NODEEDITOR_LEFT).width();
                var containerDom = that.getContainerDom();

                /** x좌표가 0 이하 일때 */
                if (x < 0) {
                    x = 0;
                }
                /** x좌표가 editor 화면의 maxWidth 이상 일때 */
                if (x > maxWidth - $(containerDom).width()) {
                    x = maxWidth - $(containerDom).width();
                }
                /** y좌표가 editor 화면의 maxHeight 이상 일때 */
                if (y > maxHeight - $(containerDom).height() ) {
                    y = maxHeight - $(containerDom).height();
                }
                /** y좌표가 0 이하 일때 */
                if (y < 0) {
                    y = 0;
                }
            

                $(oldMainDom).css('transform', `translate(0px, 0px)`); 

                var blockList = blockContainerThis.getBlockList();
                blockList.forEach(block => {
                    $(block.getMainDom()).css('transform', `translate(0px, 0px)`); 
                });

                var rootBlockList = blockContainerThis.getRootBlockList();
                shadowBlockList.forEach(shadowBlock => {
                    if ( $(shadowBlock.getMainDom()).hasClass(STR_CSS_CLASS_VP_SELECTED_SHADOWBLOCK) ) {
                        selectedBlock = shadowBlock.getSelectBlock();
                    } 
                });

                rootBlockList.forEach(rootBlock => {
                    var rootBlockContainerDom = rootBlock.getContainerDom();
                    $(rootBlockContainerDom).find(STR_CSS_CLASS_VP_BLOCK_SHADOWBLOCK).remove();
                });



                if (selectedBlock !== null) {
                    $(oldMainDom).remove();
                    // $(rootDomElement).empty();

                    $(tempChildListDom).remove();
                    $(tempChildListDom).empty();
                    
                    var childBlockList = that.selectChildBlockList();
                    childBlockList.forEach(block => {
                        var mainDom = block.getMainDom();
                        if (block.getType() === BLOCK_CODE_TYPE.NULL) {
                            $(mainDom).css(STR_OPACITY, '0');
                        } else {
                            $(mainDom).css(STR_OPACITY, '1');
                        }
                    });

                    if ((selectedBlock.getType() === BLOCK_CODE_TYPE.CLASS || selectedBlock.getType() === BLOCK_CODE_TYPE.DEF
                            || selectedBlock.getType() === BLOCK_CODE_TYPE.IF || selectedBlock.getType() === BLOCK_CODE_TYPE.FOR
                            || selectedBlock.getType() === BLOCK_CODE_TYPE.WHILE || selectedBlock.getType() === BLOCK_CODE_TYPE.TRY
                            || selectedBlock.getType() === BLOCK_CODE_TYPE.ELSE || selectedBlock.getType() === BLOCK_CODE_TYPE.ELIF
                            || selectedBlock.getType() === BLOCK_CODE_TYPE.FOR_ELSE || selectedBlock.getType() === BLOCK_CODE_TYPE.EXCEPT 
                            || selectedBlock.getType() === BLOCK_CODE_TYPE.FINALLY)
                            && selectedBlock.getNullBlock() !== null) {
                        selectedBlock.getNullBlock().deleteBlockOne();
                        selectedBlock.setNullBlock(null);
                    } 

                    selectedBlock.appendBlock(that, selectedBlockDirection);

                    {
                        var myContainerDom = that.getContainerDom();
                        $(myContainerDom).remove();
                        $(myContainerDom).empty();
                    }

                    var _containerDom = selectedBlock.getRootBlock().getContainerDom();

                    var rootBlock = selectedBlock.getRootBlock();
                    var containerDom = document.createElement(STR_DIV);
                    containerDom.classList.add(STR_CSS_CLASS_VP_BLOCK_CONTAINER);
                    $(containerDom).css(STR_TOP,`${rootBlock.getContainerPointY()}` + STR_PX);
                    $(containerDom).css(STR_LEFT,`${rootBlock.getContainerPointX()}` + STR_PX);
                    rootBlock.setContainerDom(containerDom);

                    var rootBlockStackList = rootBlock.renderChildBlockListIndentAndGet();
                    rootBlockStackList.forEach((block,index) => {
                        var blockCodeType = block.getType();
                        if (block.getUUID() === that.getUUID()) {
                            $(newMainDom).css(STR_POSITION, STR_RELATIVE);
                            $(newMainDom).css(STR_TOP,`${0}` + STR_PX);
                            $(newMainDom).css(STR_LEFT,`${0}` + STR_PX);

                            $(containerDom).append(newMainDom);

                            if (( blockCodeType === BLOCK_CODE_TYPE.CLASS || blockCodeType === BLOCK_CODE_TYPE.DEF || blockCodeType === BLOCK_CODE_TYPE.IF ||
                                blockCodeType === BLOCK_CODE_TYPE.FOR || blockCodeType === BLOCK_CODE_TYPE.WHILE || blockCodeType === BLOCK_CODE_TYPE.TRY
                                || blockCodeType === BLOCK_CODE_TYPE.ELSE || blockCodeType === BLOCK_CODE_TYPE.ELIF || blockCodeType === BLOCK_CODE_TYPE.FOR_ELSE 
                                || blockCodeType === BLOCK_CODE_TYPE.EXCEPT || blockCodeType === BLOCK_CODE_TYPE.FINALLY)
                                && block.getNullBlock() === null) {
    
                                var is = block.getNextBlockList().some(nextBlock => {
                                    if (nextBlock.getDirection() === BLOCK_DIRECTION.INDENT) {
                                        return true;
                                    }
                                });
                                if (is === false) {
                                    var nullBlock = mapTypeToBlock(blockContainerThis, BLOCK_CODE_TYPE.NULL, {pointX: 0, pointY: 0});
                                    block.setNullBlock(nullBlock);
                                    block.appendBlock(nullBlock, BLOCK_DIRECTION.INDENT);
                                    $(containerDom).append(block.getNullBlock().getMainDom());
                                    $(containerDom).append(block.getHolderBlock().getMainDom());
                                }
                            }

                            that.setMainDom(newMainDom);
                            that.bindEventAll();
                            return;
                        }

                        var mainDom = block.getMainDom();
                        $(mainDom).css(STR_TOP,`${0}` + STR_PX);
                        $(mainDom).css(STR_LEFT,`${0}` + STR_PX);
                        $(containerDom).append(mainDom);
                        
                        if ((blockCodeType === BLOCK_CODE_TYPE.CLASS || blockCodeType === BLOCK_CODE_TYPE.DEF || blockCodeType === BLOCK_CODE_TYPE.IF ||
                            blockCodeType === BLOCK_CODE_TYPE.FOR || blockCodeType === BLOCK_CODE_TYPE.WHILE || blockCodeType === BLOCK_CODE_TYPE.TRY
                            || blockCodeType === BLOCK_CODE_TYPE.ELSE || blockCodeType === BLOCK_CODE_TYPE.ELIF || blockCodeType === BLOCK_CODE_TYPE.FOR_ELSE 
                            || blockCodeType === BLOCK_CODE_TYPE.EXCEPT || blockCodeType === BLOCK_CODE_TYPE.FINALLY)
                            && block.getNullBlock() === null) {
        
                            var is = block.getNextBlockList().some(nextBlock => {
                                if (nextBlock.getDirection() === BLOCK_DIRECTION.INDENT) {
                                    return true;
                                }
                            });
                            if (is === false) {
                                var nullBlock = mapTypeToBlock(blockContainerThis, BLOCK_CODE_TYPE.NULL, {pointX: 0, pointY: 0});
                                block.setNullBlock(nullBlock);
                                block.appendBlock(nullBlock, BLOCK_DIRECTION.INDENT);
                                $(containerDom).append(block.getNullBlock().getMainDom());
                                $(containerDom).append(block.getHolderBlock().getMainDom());
                            }
                        }

                        block.bindEventAll();
                    });

                    $(STR_CSS_CLASS_VP_NODEEDITOR_LEFT).append(containerDom);
        
                    $(_containerDom).remove();
                    $(_containerDom).empty();

                    that.bindEventAll();
                    that.reRender();
                } else {
                    $(oldMainDom).remove();
                    $(oldMainDom).empty();
            
                    $(tempChildListDom).remove();
                    $(tempChildListDom).empty();

                    {
                        var _containerDom = that.getContainerDom();
                        $(_containerDom).empty();
                        $(_containerDom).remove();
                    }

                    var containerDom = document.createElement(STR_DIV);
                    containerDom.classList.add(STR_CSS_CLASS_VP_BLOCK_CONTAINER);
                    that.setContainerDom(containerDom);

                    var renderedBlockList = that.renderChildBlockListIndentAndGet();
                    renderedBlockList.forEach((block,index) => {
                        /** FIXME: */
                        if (index === 0) {
                            $(containerDom).css(STR_TOP,`${y}` + STR_PX);
                            $(containerDom).css(STR_LEFT,`${x}` + STR_PX);
                            $(newMainDom).css(STR_POSITION, STR_STATIC);
                            $(newMainDom).css(STR_TOP,`${0}` + STR_PX);
                            $(newMainDom).css(STR_LEFT,`${0}` + STR_PX);
                            $(containerDom).append(newMainDom);

                            that.setMainDom(newMainDom);
                            that.bindEventAll();

                            return;
                        }

                        var mainDom = block.getMainDom();
                        $(mainDom).css(STR_TOP,`${0}` + STR_PX);
                        $(mainDom).css(STR_LEFT,`${0}` + STR_PX);

                        $(containerDom).append(mainDom);
                        block.bindEventAll();
                    });

                    var childBlockList = that.selectChildBlockList();
                    childBlockList.forEach(block => {
                        var mainDom = block.getMainDom();
                        if (block.getType() === BLOCK_CODE_TYPE.NULL) {
                            $(mainDom).css(STR_OPACITY, '0');
                        } else {
                            $(mainDom).css(STR_OPACITY, '1');
                        }
                    });
                    
                    that.setContainerPointX(x);
                    that.setContainerPointY(y);

                    $(STR_CSS_CLASS_VP_NODEEDITOR_LEFT).append(containerDom);
                    that.untactBlock(x,y);

                }


                var blockList = blockContainerThis.getBlockList();
                blockList.forEach((block, index) => {
                    if ( block.getNullBlock() ) {
                        $(block.getNullBlock().getMainDom()).css(STR_DISPLAY,STR_BLOCK); 
                    }
                });
                blockContainerThis.renderBlockLeftHolderListHeight();
                
                that.renderResetColor();
                that.renderClickColor();
            }
        });
    }

    Block.prototype.renderClickColor = function() {
        var that = this;
        var mainDom = this.getMainDom();
        $(mainDom).css(STR_BORDER,'2px solid yellow');
        $(mainDom).find(STR_CSS_CLASS_VP_BLOCK_LEFT_HOLDER).css(STR_BACKGROUND_COLOR,'yellow');
        $(mainDom).find(STR_CSS_CLASS_VP_BLOCK_LEFT_HOLDER).css('box-shadow','0 1px 4px rgba(0, 0, 0, .6)');
        if (that.getHolderBlock()) {
            $(that.getHolderBlock().getMainDom()).css('box-shadow','0 1px 4px rgba(0, 0, 0, .6)');
            $(that.getHolderBlock().getMainDom()).css(STR_BORDER,'2px solid yellow');
        }
    }

    Block.prototype.bindClickEvent = function() {
        var that = this;
        var blockContainerThis = that.getBlockContainerThis();
        var mainDom = that.getMainDom();

        var deleteBtn = $(`<div class='vp-block-delete-btn'>x</div>`);
        var blockCodeType = this.getType();
        if (blockCodeType === BLOCK_CODE_TYPE.CLASS || blockCodeType === BLOCK_CODE_TYPE.DEF ) {
            $(deleteBtn).css(STR_BACKGROUND_COLOR,`${COLOR_BLUE}`);
        } else if ( blockCodeType === BLOCK_CODE_TYPE.IF ||
            blockCodeType === BLOCK_CODE_TYPE.FOR || blockCodeType === BLOCK_CODE_TYPE.WHILE || blockCodeType === BLOCK_CODE_TYPE.TRY
            || blockCodeType === BLOCK_CODE_TYPE.ELSE || blockCodeType === BLOCK_CODE_TYPE.ELIF || blockCodeType === BLOCK_CODE_TYPE.FOR_ELSE 
            || blockCodeType === BLOCK_CODE_TYPE.EXCEPT || blockCodeType === BLOCK_CODE_TYPE.FINALLY) {
            $(deleteBtn).css(STR_BACKGROUND_COLOR,`${COLOR_RED}`);
        } else {
            $(deleteBtn).css(STR_BACKGROUND_COLOR,`${COLOR_GREEN}`);
        }

        $(mainDom).click(function(event){
            that.renderResetColor();
            that.renderClickColor();

            that.renderBottomOption();
            var blockList = blockContainerThis.getBlockList();
            blockList.forEach(block => {
                var mainDom = block.getMainDom();
                $(mainDom).find(STR_CSS_CLASS_VP_BLOCK_DELETE_BTN).remove();
            });
            $(mainDom).append(deleteBtn);

            blockContainerThis.renderBlockLeftHolderListHeight();
        });

        $(deleteBtn).click(function(event) { 
            that.deleteBlock();
            $(that.getContainerDom()).remove();
        });
    }


        /** routrMapApi */
    var BLOCK_MAP = new Map();
    BLOCK_MAP.set(BLOCK_CODE_TYPE.CLASS, Block);
    BLOCK_MAP.set(BLOCK_CODE_TYPE.DEF, Block);
    BLOCK_MAP.set(BLOCK_CODE_TYPE.IF, Block);
    BLOCK_MAP.set(BLOCK_CODE_TYPE.FOR, Block);
    BLOCK_MAP.set(BLOCK_CODE_TYPE.WHILE, Block);
    BLOCK_MAP.set(BLOCK_CODE_TYPE.IMPORT, Block);
    BLOCK_MAP.set(BLOCK_CODE_TYPE.TRY, Block);
    BLOCK_MAP.set(BLOCK_CODE_TYPE.API, Block);

    BLOCK_MAP.set(BLOCK_CODE_TYPE.RETURN, Block);
    BLOCK_MAP.set(BLOCK_CODE_TYPE.BREAK, Block);
    BLOCK_MAP.set(BLOCK_CODE_TYPE.CONTINUE, Block);
    BLOCK_MAP.set(BLOCK_CODE_TYPE.PASS, Block);

    BLOCK_MAP.set(BLOCK_CODE_TYPE.ELIF, Block);
    BLOCK_MAP.set(BLOCK_CODE_TYPE.ELSE, Block);
    BLOCK_MAP.set(BLOCK_CODE_TYPE.FOR_ELSE, Block);

    BLOCK_MAP.set(BLOCK_CODE_TYPE.INIT, Block);
    BLOCK_MAP.set(BLOCK_CODE_TYPE.DEL, Block);
    BLOCK_MAP.set(BLOCK_CODE_TYPE.EXCEPT, Block);
    BLOCK_MAP.set(BLOCK_CODE_TYPE.FINALLY, Block);

    BLOCK_MAP.set(BLOCK_CODE_TYPE.CODE, Block);
    BLOCK_MAP.set(BLOCK_CODE_TYPE.HOLDER, Block);
    BLOCK_MAP.set(BLOCK_CODE_TYPE.NULL, Block);
    var mapTypeToBlock = function(blockContainerThis, enumData, pointObj) {
        if (BLOCK_MAP.has(enumData)) {
            var blockConstructor = BLOCK_MAP.get(enumData);
            return new blockConstructor(blockContainerThis, enumData, pointObj)
        } else {
            alert('존재하지 않는 BLOCK ENUM 입니다');
        }
    }

    return {
        Block, mapTypeToBlock
    };
});
