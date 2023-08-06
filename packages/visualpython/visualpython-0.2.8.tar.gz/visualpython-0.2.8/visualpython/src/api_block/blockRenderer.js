define([
    './constData.js'
], function ( constData ) {
    const {BLOCK_CODE_TYPE
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
            , STATE_customCodeLine } = constData;
    var renderMainDom = function() {
        var mainDom = document.createElement('div');
        mainDom.classList.add('vp-block');
        return mainDom;
    }

    var renderMainInnerDom = function() {
        var mainInnerDom = $(`<div class='vp-block-inner'></div>`);
        return mainInnerDom;
    }

    var generateClassInParamList = function(that) {
        var classInParamList = that.getState(STATE_classInParamList);
        var classInParamStr = `(`;
        classInParamList.forEach((classInParam, index ) => {
            classInParamStr += `${classInParam}`;
            if (that.getState(STATE_classInParamList).length - 1 !== index ) {
                classInParamStr += `, `;
            }
        });
        classInParamStr += `) : `;
        return classInParamStr;
    }

    var generateDefInParamList = function(that) {
        /** 함수 파라미터 */
        var defInParamList = that.getState(STATE_defInParamList);
        var defInParamStr = `(`;
        defInParamList.forEach((defInParam, index ) => {
            defInParamStr += `${defInParam}`;
            if (that.getState(STATE_defInParamList).length - 1 !== index ) {
                defInParamStr += `, `;
            }
        });
        defInParamStr += `) : `;
        return defInParamStr;
    }

    var generateReturnOutParamList = function(that) {
        var returnOutParamList = that.getState(STATE_returnOutParamList);
        var returnOutParamStr = ` `;
        returnOutParamList.forEach((defInParam, index ) => {
            returnOutParamStr += `${defInParam}`;
            if (that.getState(STATE_returnOutParamList).length - 1 !== index ) {
                returnOutParamStr += `, `;
            }
        });
        returnOutParamStr += ``;
        return returnOutParamStr;
    }

    var renderMainHeaderDom = function(that) {
        /** 클래스 이름 */
        var className = that.getState(STATE_className);
        var classInParamList = that.getState(STATE_classInParamList);
        /** 클래스 파라미터 */
        var classInParamStr = generateClassInParamList(that);
        /** 함수 이름 */
        var defName = that.getState(STATE_defName);
        var defInParamList = that.getState(STATE_defInParamList);
        /** 함수 파라미터 */
        var defInParamStr = generateDefInParamList(that);
        /** return */
        var returnOutParamList = that.getState(STATE_returnOutParamList);
        var returnOutParamStr = generateReturnOutParamList(that);

        var blockName = that.getName();
        var blockUUID = that.getUUID();
        var mainHeaderDom = $(`<div class='vp-block-header'>
                                <strong class="vp-nodeeditor-style-flex-column-center ${that.getType() !== BLOCK_CODE_TYPE.HOLDER 
                                                                                                ? 'vp-block-name' : ''}" 
                                    style="margin-right:10px; 
                                        font-size:12px; 
                                        color:#252525;">
                                    ${blockName}
                                </strong>
                                <div class='vp-nodeeditor-codeline-ellipsis 
                                            vp-nodeeditor-codeline-container-box'>
                                    <div class='vp-nodeeditor-style-flex-row'>
                                                <div class='vp-block-header-class-name-${blockUUID}'
                                                    style='font-size:12px;'>
                                                    ${className}
                                                </div>
                                                <div class='vp-block-header-class-param-${blockUUID}'
                                                    style='font-size:12px;'>
                                                    ${classInParamList.length === 0 
                                                        ? ''
                                                        : classInParamStr}
                                                </div>
                                            </div>
                                            <div class='vp-nodeeditor-style-flex-row'>
                                                <div class='vp-block-header-def-name-${blockUUID}'
                                                    style='font-size:12px;'>
                                                    ${defName}
                                                </div>
                                                <div class='vp-block-header-def-param-${blockUUID}'
                                                        style='font-size:12px;'>
                                                        ${defInParamList.length === 0 
                                                            ? ''
                                                            : defInParamStr}
                                                </div>
                                            </div>
                                            <div class='vp-block-header-if-code-${blockUUID}'
                                                style='font-size:12px;'>
                                                ${that.getState(STATE_ifCodeLine)}
                                            </div>
                                            <div class='vp-block-header-for-code-${blockUUID}'
                                                style='font-size:12px;'>
                                                ${that.getState(STATE_forCodeLine)}
                                            </div>
                                            <div class='vp-block-header-while-code-${blockUUID}'
                                                style='font-size:12px;'>
                                                ${that.getState(STATE_whileCodeLine)}
                                            </div>
                                            <div class='vp-block-header-elif-code-${blockUUID}'
                                                style='font-size:12px;'>
                                                ${that.getState(STATE_elifCodeLine)}
                                            </div>
                                            <div class='vp-block-header-except-code-${blockUUID}'
                                                style='font-size:12px;'>
                                                ${that.getState(STATE_exceptCodeLine)}
                                            </div>
                                            <div class='vp-block-header-custom-code-${blockUUID}'
                                                style='font-size:12px;'>
                                                ${that.getState(STATE_customCodeLine)}
                                            </div>
                                            <div class='vp-block-header-return-param-${blockUUID}'
                                                    style='font-size:12px;'>
                                                ${returnOutParamList.length === 0 
                                                        ? ''
                                                        : returnOutParamStr}
                                            </div>
                                        </div>
                                </div>`);
        return mainHeaderDom;
    }

    var renderBottomOptionContainer = function() {
        return $(`<div class='vp-nodeeditor-style-flex-row-center' 
                        style='padding: 0.5rem;'></div>`);
    }

    var renderBottomOptionContainerInner = function() {
        return $(`<div class='vp-nodeeditor-blockoption 
                            vp-nodeeditor-option'
                    style='width: 95%;'>
                </div>`);
    }

    var renderDomContainer = function() {
        var domContainer = $(`<div class='vp-nodeeditor-option-container'>
                                        <div class='vp-nodeeditor-tab-navigation-node-block-title'>
                                            <span class='vp-block-optiontab-name'>code</span>
                                            <div class='vp-nodeeditor-style-flex-row-center'>
                                                <div class='vp-nodeeditor-option-vertical-btn'>▼</div>
                                            </div>
                                        </div>
                                    </div>`);
        return domContainer;
    }

    var renderBottomOptionInnerDom = function() {
        var innerDom = $(`<div class='vp-nodeeditor-option-container'>
                                    <div class='vp-nodeeditor-tab-navigation-node-block-title'>
                                        <span class='vp-block-optiontab-name'>name</span>
                                        <div class='vp-nodeeditor-style-flex-row-center'>
                                            <div class='vp-nodeeditor-option-vertical-btn'>▼</div>
                                        </div>
                                    </div>
                                </div>`);
        return innerDom;
    }

    var renderBottomOptionName = function(name, blockCodeType, uuid) {
        var classStr = ``;

        if (blockCodeType === BLOCK_CODE_TYPE.CLASS) {
            classStr = `vp-nodeeditor-input-class-name`;
        } else if (blockCodeType === BLOCK_CODE_TYPE.DEF) {
            classStr = `vp-nodeeditor-input-def-name`;
        } else if (blockCodeType === BLOCK_CODE_TYPE.IF) {
            classStr = 'vp-nodeeditor-if-input';
        } else if (blockCodeType === BLOCK_CODE_TYPE.FOR) {
            classStr = 'vp-nodeeditor-for-input';
        } else if (blockCodeType === BLOCK_CODE_TYPE.WHILE) {
            classStr = 'vp-nodeeditor-while-input';
        } else if (blockCodeType === BLOCK_CODE_TYPE.CODE) {
            classStr = 'vp-nodeeditor-code-input';
        } else if (blockCodeType === BLOCK_CODE_TYPE.ELIF) {
            classStr = `vp-nodeeditor-elif-input-${uuid}`;
        }

        var nameDom = $(`<div class='vp-block-blockoption 
                                    vp-nodeeditor-blockoption-block 
                                    vp-nodeeditor-blockoption-inner vp-nodeeditor-style-flex-row' 
                                style='position:relative;'>
                            <div class='vp-nodeeditor-blockoption-header'>
                                <div class='vp-nodeeditor-blockoption-codeline'>
                                    <input class='vp-nodeeditor-blockoption-input ${classStr}' 
                                            value='${name}' 
                                            placeholder='input class name' ></input>
                                </div>
                            </div>                                                          
                        </div>`);
        return nameDom;
    }

    var renderInParamContainer = function(inParamList, blockCodeType) {
        if (blockCodeType === BLOCK_CODE_TYPE.CLASS) {
            classStr = `vp-nodeeditor-class-inparam-plus-btn`;
        } else if (blockCodeType === BLOCK_CODE_TYPE.DEF) {
            classStr = `vp-nodeeditor-def-inparam-plus-btn`;
        } else if (blockCodeType === BLOCK_CODE_TYPE.RETURN) {
            classStr = `vp-nodeeditor-return-outparam-plus-btn`;
        }

        var inParamContainer = $(`<div class='vp-nodeeditor-ifoption-container'>
                                            <div class='vp-nodeeditor-tab-navigation-node-block-title'>
                                                <span class='vp-block-optiontab-name'>
                                                    in param</span>
                                                <div class='vp-nodeeditor-style-flex-row-center' >
                                                    <span class='vp-nodeeditor-number'
                                                        style='margin-right:5px;'>
                                                        ${inParamList.length} Param
                                                    </span>
                                                    <button class='vp-block-btn ${classStr}'
                                                            style='margin-right:5px;'>
                                                        + param
                                                    </button>
                                                    <div class='vp-nodeeditor-option-vertical-btn'>▼</div>
                                                </div>
                                            </div>
                                        </div>`);
        return inParamContainer;
    }

    var renderInParamDom = function(inParam, index, blockCodeType, uuid) {
        var classStr = ``;
        if (blockCodeType === BLOCK_CODE_TYPE.CLASS) {
            classStr = `vp-nodeeditor-input-class-inparam-${index}`;
        } else if (blockCodeType === BLOCK_CODE_TYPE.DEF) {
            classStr = `vp-nodeeditor-input-def-inparam-${index}'`;
        } else if (blockCodeType === BLOCK_CODE_TYPE.RETURN) {
            classStr = `vp-nodeeditor-return-outparam-${index}`;
        } else if (blockCodeType === BLOCK_CODE_TYPE.EXCEPT) {
            classStr = `vp-nodeeditor-except-input-${index}`;
        } else if (blockCodeType === BLOCK_CODE_TYPE.ELIF) {
            classStr = `vp-nodeeditor-elif-input-${uuid}`;
        }

        var inParamDom = $(`<div class='vp-nodeeditor-style-flex-row'>
                                <div class='vp-nodeeditor-style-flex-column-center'
                                    style='margin:0 0.5rem; '>
                                    ${index+1}
                                </div>
                                <div class='vp-nodeeditor-blockoption-block
                                            vp-nodeeditor-blockoption-inner vp-nodeeditor-style-flex-row' 
                                        style='position:relative'>
                                    <div class='vp-nodeeditor-blockoption-header'>

                                        <div class='vp-nodeeditor-blockoption-codeline'>
                                            <input placeholder='input param' 
                                                class='vp-nodeeditor-blockoption-input ${classStr}' 
                                                value='${inParam}'>
                                        </div>
                                    </div>                                                          
                                </div>
                            </div>`);
        return inParamDom;
    }

    var renderBottomOptionTitle = function(title) {
        var titleDom = $(`<div class='vp-nodeeditor-option-container'
                            style='margin-top:5px;'>
                                <div class='vp-nodeeditor-tab-navigation-node-block-title'>
                                    <span class='vp-block-optiontab-name'>${title}</span>
                                    <div class='vp-nodeeditor-style-flex-row-center'>
                                        <div class='vp-nodeeditor-option-vertical-btn'>▼</div>
                                    </div>
                                </div>
                            </div>`);
        return titleDom;
    }

    var renderElseBlock = function(that, blockCodeType) {
        var state;
        if (blockCodeType === BLOCK_CODE_TYPE.IF) {
            state = that.getState(STATE_isIfElse);
        } else {
            state = that.getState(STATE_isForElse);
        }
        // console.log('state', state);
        var uuid = that.getUUID();
        var elseBlock = $(`<div class='vp-nodeeditor-option-container'
                                style='margin-top:5px;'>
                                <div class='vp-nodeeditor-tab-navigation-node-block-title'>
                                    <span class='vp-block-optiontab-name'>else</span>
                                    <div class='vp-nodeeditor-style-flex-row-center'>
                                        <div style='display:flex; margin-right: 5px;'>
                                            <div style='margin-top: 2.5px;
                                                        margin-right: 5px;'>yes</div>
                                            <input class='vp-nodeeditor-else-yes-${uuid}'
                                                style='margin-top: 6px;' 
                                                ${state === true 
                                                        ? 'checked'
                                                        : '' }
                                                type='checkbox'/>
                                        </div>
                                        <div style='display:flex; margin-right: 5px;'>
                                            <div style='margin-top: 2.5px;
                                                        margin-right: 5px;'>no</div>
                                            <input class='vp-nodeeditor-else-no-${uuid}'
                                                style='margin-top: 6px;' 
                                                ${state === false 
                                                        ? 'checked'
                                                        : '' }
                                                type='checkbox'/>
                                        </div>
                                        <div class='vp-nodeeditor-option-vertical-btn'>▼</div>
                                    </div>
                                </div>
                            </div>`);
        return elseBlock;
    }

    var renderDefaultOrDetailButton = function(uuid) {

        var defaultOrDetailButton = $(`<div class='vp-nodeeditor-style-flex-row-between'>
                                            <button class='vp-nodeeditor-default-option-${uuid} 
                                                        vp-nodeeditor-default-detail-option-btn
                                                        vp-nodeeditor-option-btn-selected'>
                                                    Default Option
                                            </button>
                                            <button class='vp-nodeeditor-detail-option-${uuid} 
                                                        vp-nodeeditor-default-detail-option-btn'>
                                                    Detail Option
                                            </button>
                                        </div>`);
        return defaultOrDetailButton;
    }

    return {
        renderMainDom
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
        , generateReturnOutParamList
    }

});