define([
    'require'
    , 'jquery'
    , 'nbextensions/visualpython/src/common/vpCommon'
    , 'nbextensions/visualpython/src/common/constant'
    , 'nbextensions/visualpython/src/common/StringBuilder'
    , 'nbextensions/visualpython/src/common/vpFuncJS'
    , 'nbextensions/visualpython/src/common/vpSetting'
    // TEST: CodeMirror
    , 'codemirror/lib/codemirror'
    , 'codemirror/mode/python/python'
    , 'notebook/js/codemirror-ipython'
    , 'codemirror/addon/display/placeholder'
], function (requirejs, $, vpCommon, vpConst, sb, vpFuncJS, vpSetting, CodeMirror, cmpython, cmip) {
    // 옵션 속성
    const funcOptProp = {
        stepCount : 1
        , funcName : "Option"
        , funcID : "com_option"
    }

    /**
     * html load 콜백. 고유 id 생성하여 부과하며 js 객체 클래스 생성하여 컨테이너로 전달
     * @param {function} callback 호출자(컨테이너) 의 콜백함수
     */
    var optionLoadCallback = function(callback) {
        // document.getElementsByTagName("head")[0].appendChild(link);
        // 컨테이너에서 전달된 callback 함수가 존재하면 실행.
        if (typeof(callback) === 'function') {
            var uuid = vpCommon.getUUID();
            // 최대 10회 중복되지 않도록 체크
            for (var idx = 0; idx < 10; idx++) {
                // 이미 사용중인 uuid 인 경우 다시 생성
                if ($(vpConst.VP_CONTAINER_ID).find("." + uuid).length > 0) {
                    uuid = vpCommon.getUUID();
                }
            }
            $(vpCommon.wrapSelector(vpConst.OPTION_GREEN_ROOM)).find(vpConst.OPTION_PAGE).addClass(uuid);
            // 옵션 객체 생성
            var optionPackage = new OptionPackage(uuid);
            // 옵션 속성 할당.
            optionPackage.setOptionProp(funcOptProp);
            // html 설정.
            optionPackage.initHtml();
            callback(optionPackage);  // 공통 객체를 callback 인자로 전달

            // after load cell metadata, set codemirror value
            // optionPackage.vp_userCode.setValue($(vpCommon.wrapSelector('#vp_userCode')).val());
            optionPackage.bindCodeMirror();
        }
    }
    
    /**
     * html 로드. 
     * @param {function} callback 호출자(컨테이너) 의 콜백함수
     */
    var initOption = function(callback) {
        vpCommon.loadHtml(vpCommon.wrapSelector(vpConst.OPTION_GREEN_ROOM), "file_io/option.html", optionLoadCallback, callback);
    }

    /**
     * 본 옵션 처리 위한 클래스
     * @param {String} uuid 고유 id
     */
    var OptionPackage = function(uuid) {
        this.uuid = uuid;   // Load html 영역의 uuid.
        this.package = {
            input: [
                { name: 'vp_userCode' }
            ]
        }
    }

    /**
     * vpFuncJS 에서 상속
     */
    OptionPackage.prototype = Object.create(vpFuncJS.VpFuncJS.prototype);

    /**
     * 유효성 검사
     * @returns 유효성 검사 결과. 적합시 true
     */
    OptionPackage.prototype.optionValidation = function() {
        return true;

        // 부모 클래스 유효성 검사 호출.
        // vpFuncJS.VpFuncJS.prototype.optionValidation.apply(this);
    }


    /**
     * html 내부 binding 처리
     */
    OptionPackage.prototype.initHtml = function() {
        // bind values after loading html
        this.package.input && this.package.input.forEach(obj => {
            if (obj.value != undefined) {
                var tag = $(this.wrapSelector('#' + obj.name));
                tag.val(obj.value);
            }
        });
    }

    /**
     * TEST: Bind CodeMirror to Textarea
     */
    OptionPackage.prototype.bindCodeMirror = function() {
        this.vp_userCode = CodeMirror.fromTextArea($(this.wrapSelector('#vp_userCode'))[0], {
            mode: {
                name: 'python',
                version: 3,
                singleLineStringErrors: false
            },  // text-cell(markdown cell) set to 'htmlmixed'
            indentUnit: 4,
            matchBrackets: true,
            lineNumbers: true,
            autoRefresh:true,
            lineWrapping: true, // text-cell(markdown cell) set to true
            theme: "default",
            extraKeys: {"Enter": "newlineAndIndentContinueMarkdownList"}
        });
        this.vp_userCode.setValue($(this.wrapSelector('#vp_userCode')).val());

        // focus on codemirror
        this.vp_userCode.focus();

        /**
         * CodeMirror reference : https://codemirror.net/index.html
         *  
         * CodeMirror object Usage :
         * 1. Get value
         *  vp_testCodeMirror.getValue()
         * 2. Set value
         *  vp_testCodeMirror.setValue('string')
         * 3. Apply to original textarea
         *  vp_testCodeMirror.save()
         * 4. Get Textarea object
         *  vp_testCodeMirror.getTextArea()
         * 
         * Prefix box Textarea
         *  var vp_prefix = CodeMirror.fromTextArea($('#vp_prefixBox textarea')[0], { mode:'htmlmixed', lineNumbers: true, theme: 'default'});
         * Postfix box Textarea
         *  var vp_postfix = CodeMirror.fromTextArea($('#vp_postfixBox textarea')[0], { mode: 'htmlmixed', lineNumbers: true, theme: 'default'});
         */
    }

    /**
     * 코드 생성
     * @param {boolean} exec 실행여부
     */
    OptionPackage.prototype.generateCode = function(exec) {
        if (!this.optionValidation()) return;
        
        var sbCode = new sb.StringBuilder();
        sbCode.append(this.vp_userCode.getValue());

        // save codemirror value to origin textarea
        this.vp_userCode.save();

        this.cellExecute(sbCode.toString(), exec);
    }

    return {
        initOption: initOption
    };
});
