# SIC-Assembler

## pass1:

 將SIC/XE組合語言讀入，並將每句的token切出來存於list內
 
 將其每一個token根據其出現的位置與table1和table2的內容分類成instruction/pesudo/literal/symbol
 
 根據初始位置計算location，透過dictionary以symbol為key，location為value建立symbol table
 
 此階段下若讀到已在symbol table內出現的symbol會發生

## pass2:

 token已分類好的程式碼再次讀入
 
 根據不同的指令格式與定址模式將指令翻譯為object code
 
 再透過location算出不同format下的address
 
 此階段下若讀到未在symbol table內出現的symbol會發生undefined
