module FA_BL(S, C, a, b, c);
    input a,b,c;
    output reg S,C;

    always @({a,b,c}) begin
        {S,C} = a + b + c;
    end
endmodule

module FA_BL_tb;
    reg a,b,c;
    wire S,C;
    integer i;

    FA_BL inst(S, C, a, b, c);

    initial begin
        $monitor("A=%0b|B=%0b|Cin=%0b|S=%0b|Cout=%0b", a,b,c,S,C);
        for(i=0;i<8;i=i+1) begin
            {a,b,c} = i;
            #10;
        end
    end

endmodule
    
