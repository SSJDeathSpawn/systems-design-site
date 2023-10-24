module FS_SL(B,D,a,b,c);
    input a,b,c;
    output B,D;

    always @({a,b,c}) begin
        {B,D} = a-b-c;
    end
endmodule

module FS_SL_tb;
    reg a,b,c;
    wire B,D;
    integer i;

    FS_SL inst(B,D,a,b,c);

    initial begin
        $monitor("A=%0b|B=%0b|C=%0b|Borrow=%0b|Diff=%0b",a,b,c,B,D);
        for(i=0;i<8;i=i+1) begin
            {a,b,c}=i;
            #10;
        end
    end
endmodule
