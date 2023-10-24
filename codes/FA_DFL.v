module FA_DFL(S, C, a, b, c);
    input a, b, c;
    output S, C;
    
    assign S = a ^ b ^ c;
    assign C = (a ^ b) & c | (a & b);

endmodule

module FA_DFL_tb;
    reg a,b,c;
    wire S,C;
    integer i;

    FA_DFL inst(S, C, a, b, c);

    initial begin
        $monitor("A=%0b|B=%0b|Cin=%0b|S=%0b|Cout=%0b", a,b,c,S,C);
        for(i=0;i<8;i=i+1) begin
            {a,b,c} = i;
            #10;
        end
    end

endmodule
    
