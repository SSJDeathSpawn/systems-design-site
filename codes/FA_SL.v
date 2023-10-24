module FA_SL(S,C,a,b,c);
	input a,b,c;
	output S,C;
	wire bc_add, bc_and, ax;
	xor xor1(bc_add, b,c);
	xor xor2(S, a,bc_add);
	and and1(ax, a, bc_add);
	and and2(bc_and, b, c);	
	or or1(C, bc_and, ax);
endmodule

module FA_SL_tb;
    reg a,b,c;
    wire S,C;
    integer i;

    FA_SL inst(S, C, a, b, c);

    initial begin
        $monitor("A=%0b|B=%0b|Cin=%0b|S=%0b|Cout=%0b", a,b,c,S,C);
        for(i=0;i<8;i=i+1) begin
            {a,b,c} = i;
            #10;
        end
    end

endmodule
    
