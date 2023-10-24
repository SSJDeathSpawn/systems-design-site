module FS_SL(B,D,a,b,c);
    input a,b,c;
    output B,D;
    wire a_not, bc_xor,bc_and, bc_xnor, ax_not, a_notx;
	not not1(a_not, a);
	xor xor1(bc_xor, b,c);
	not not2(bc_xnor, bc_xor);
	and and1(ax_not, a, bc_xnor);
	and and2(a_notx, a_not, bc_xor);
	or or1(D, a_notx, ax_not);
	and and3(bc_and, b, c);
	or or2(B, bc_and, a_notx);
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
