module FS_DFL(B,D,a,b,c);
    input a,b,c;
    output B,D;
    
    assign D = a ^ b ^ c;
    assign B = (~(b^c) & a) | ((~b) & c);

endmodule

module FS_DFL_tb;
    reg a,b,c;
    wire B,D;
    integer i;

    FS_DFL inst(B,D,a,b,c);

    initial begin
        $monitor("A=%0b|B=%0b|C=%0b|Borrow=%0b|Diff=%0b",a,b,c,B,D);
        for(i=0;i<8;i=i+1) begin
            {a,b,c}=i;
            #10;
        end
    end
endmodule
