define([

], function ( ) {

    const BLOCK_CODE_BTN_TYPE = {
        CLASS: 1
        , DEF: 2
        , IF: 3
        , FOR: 4
        , WHILE: 5
        , IMPORT: 6
        , API: 7
        , TRY: 8
    
        , RETURN: 9
        , BREAK: 10
        , CONTINUE: 11
        , PASS: 12
    
        , CODE: 999
    }
    
    const BLOCK_CODE_TYPE = {
        CLASS: 1
        , DEF: 2
        , IF: 3
        , FOR: 4
        , WHILE: 5
        , IMPORT: 6
        , API: 7
        , TRY: 8
        , RETURN: 9
        , BREAK: 10
        , CONTINUE: 11
        , PASS: 12
    
        , ELIF: 100
        , ELSE: 200
        , FOR_ELSE: 201
        , INIT: 300
        , DEL: 400
        , EXCEPT: 500
        , FINALLY: 600
        , CODE: 999
        , HOLDER: 1000
        , NULL: 10000
    }
    
    const CLASS_TYPE = {
        BLOCK: 1
        , SHADOW_BLOCK: 2
        , BLOCK_CONTAINER: 3
        , CREATE_BLOCK_BTN: 100
    }
    const BLOCK_DIRECTION  = {
        ROOT: -1
        , DOWN: 1
        , INDENT: 2
        , BOTTOM_DOWN: 3
    }
    
    const BLOCK_TYPE = {
        BLOCK: 1
        , SHADOW_BLOCK: 2
        , MOVE_BLOCK: 3
    }
    
    const MAKE_CHILD_BLOCK = {
        MOVE: 1
        , SHADOW: 2
    }
    
    
    const INDENT_DEPTH_PX = 20;
    const BLOCK_HEIGHT_PX = 26;
    const MAX_ITERATION = 100;
    const NUM_ZERO = 0;
    // const 
    
    const STR_DIV = 'div';
    const STR_BORDER = 'border';
    const STR_TOP = 'top';
    const STR_LEFT = 'left';
    const STR_PX = 'px';
    const STR_OPACITY = 'opacity';
    const STR_MARGIN_TOP = 'margin-top';
    const STR_MARGIN_LEFT = 'margin-left';
    const STR_DISPLAY = 'display';
    const STR_BACKGROUND_COLOR = 'background-color';
    const STR_HEIGHT = 'height';
    const STR_YES = 'yes';
    const STR_DATA_NUM_ID = 'data-num-id';
    const STR_DATA_DEPTH_ID = 'data-depth-id';
    const STR_NONE = 'none';
    const STR_BLOCK = 'block';
    const STR_SELECTED = 'selected';
    const STR_COLON_SELECTED = ':selected';
    const STR_POSITION = 'position';
    const STR_STATIC = 'static';
    const STR_RELATIVE = 'relative';
    const STR_ABSOLUTE = 'absolute';
    
    const STR_CLASS = 'class';
    const STR_DEF = 'def';
    const STR_IF = 'if';
    const STR_FOR = 'for';
    const STR_WHILE = 'while';
    const STR_IMPORT = 'import';
    const STR_API = 'api';
    const STR_TRY = 'try';
    const STR_RETURN = 'return';
    const STR_BREAK = 'break';
    const STR_CONTINUE = 'continue';
    const STR_PASS = 'pass';
    const STR_CODE = 'code';
    
    const STR_ELIF = 'elif';
    
    const STR_CSS_CLASS_VP_BLOCK_CONTAINER = 'vp-block-container';
    
    const STR_CSS_CLASS_VP_BLOCK_NULLBLOCK = 'vp-block-nullblock';
    
    const STR_CSS_CLASS_VP_BLOCK_SHADOWBLOCK = '.vp-block-shadowblock';
    const STR_CSS_CLASS_VP_BLOCK_DELETE_BTN = '.vp-block-delete-btn';
    const STR_CSS_CLASS_VP_NODEEDITOR_LEFT = `.vp-nodeeditor-left`;
    const STR_CSS_CLASS_VP_NODEEDITOR_BOTTOM_TAB_VIEW = '.vp-nodeeditor-bottom-tab-view';
    const STR_CSS_CLASS_VP_BLOCK_LEFT_HOLDER = '.vp-block-left-holder';
    
    const STR_CSS_CLASS_VP_NODEEDITOR_MINIMIZE = 'vp-nodeeditor-minimize';
    const STR_CSS_CLASS_VP_NODEEDITOR_ARROW_UP = 'vp-nodeeditor-arrow-up';
    const STR_CSS_CLASS_VP_NODEEDITOR_ARROW_DOWN = 'vp-nodeeditor-arrow-down';
    const STR_CSS_CLASS_VP_SELECTED_SHADOWBLOCK = 'selected-shadowblock';
    
    const STR_CHANGE_KEYUP_PASTE = 'change keyup paste';
    
    const STATE_classInParamList = 'classInParamList';
    const STATE_className = 'className';
    
    const STATE_defName = 'defName';
    const STATE_defInParamList = 'defInParamList';
    
    const STATE_ifCodeLine = 'ifCodeLine';
    const STATE_isIfElse = 'isIfElse';
    const STATE_isForElse = 'isForElse';
    const STATE_elifCodeLine = 'elifCodeLine';
    const STATE_elifList = 'elifList';
    
    const STATE_forCodeLine = 'forCodeLine';
    
    const STATE_whileCodeLine = 'whileCodeLine';
    
    const STATE_baseImportList = 'baseImportList';
    const STATE_customImportList = 'customImportList';
    
    const STATE_exceptList = 'exceptList';
    const STATE_exceptCodeLine = 'exceptCodeLine';
    const STATE_isFinally = 'isFinally';
    
    const STATE_returnOutParamList = 'returnOutParamList';
    
    const STATE_customCodeLine = 'customCodeLine';
    
    const COLOR_BLUE = `#2240c5`;
    const COLOR_RED = `#cc1f1f`;
    const COLOR_GREEN = `#14c51d`;
    
    return {
        BLOCK_CODE_BTN_TYPE
        , BLOCK_CODE_TYPE
        , BLOCK_DIRECTION
        , BLOCK_TYPE
        , MAKE_CHILD_BLOCK

        , INDENT_DEPTH_PX

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
        , COLOR_GREEN
    }
});
