mode(0);
ieee(1);

a = 120; // a:: 
c = 55;
b = a*cos((20/180)*%pi)+c;
e = 187;
f = 154;
delta_d = 10;
s = 190; 
n = s/delta_d; 

theta = zeros(6,n+1); 
d = zeros(1,n+1);
E = zeros(1,n+1);
F = zeros(1,n+1);

d(1) = a*sin((20/180)*%pi);
E(1) = b^2+c^2+d(1)^2-a^2;
F(1) = a^2+c^2+d(1)^2-b^2;

wflag = 1;
i = 1;

if 4*b^2*d(1)^2+4*b^2*c^2-E(1)^2<0 then
 wflag = 0; 
end;

if 4*a^2*d(1)^2+4*a^2*c^2-F(1)^2<0 then
 wflag = 0; 
end;

while wflag==1

  theta(1,i) = %pi;
  theta(2,i) = 2*atan((1/(F(i)+2*a*c))*(-2*a*d(i)-sqrt(4*a^2*d(i)^2+4*a^2*c^2-F(i)^2)))+2*%pi;
  theta(3,i) = 2*atan((1/(E(i)-2*b*c))*(2*b*d(i)+sqrt(4*b^2*d(i)^2+4*b^2*c^2-E(i)^2)));
  theta(4,i) = (3/2)*%pi;
  theta(5,i) = theta(2,i)-(134/180)*%pi;
  theta(6,i) = theta(2,i)-(90/180)*%pi;

 i = i+1; 
 d(i) = d(i-1)+delta_d;
 E(i) = b^2+c^2+d(i)^2-a^2;
 F(i) = a^2+c^2+d(i)^2-b^2;
 //----
 if i>(n+1) then 
  wflag = 0; 
 end;
 //----
 if 4*b^2*d(i)^2+4*b^2*c^2-E(i)^2<0 then
  wflag = 0; 
 end;
 //----
 if 4*a^2*d(i)^2+4*a^2*c^2-F(i)^2<0 then
  wflag = 0; 
 end;
 //----
end;



for k = 1:i-1

 xO = 0;
 yO = 0;

 xA = -c;
 yA = 0;

 xB = xA+a*cos(theta(2,k));
 yB = yA+a*sin(theta(2,k));

 xC = 0; 
 yC = -d(k);

 xP = xA+e*cos(theta(5,k)); 
 yP = yA+e*sin(theta(5,k));

 xQ = xA+f*cos(theta(6,k)); 
 yQ = yA+f*sin(theta(6,k));

 x_AO = [xO,xA];
 y_AO = [yO,yA];

 x_BA = [xA,xB]; 
 y_BA = [yA,yB];

 x_BC = [xC,xB];
 y_BC = [yC,yB];

 x_PA = [xA,xP];
 y_PA = [yA,yP];

 x_QA = [xA,xQ];
 y_QA = [yA,yQ];

 x_PQ = [xQ,xP];
 y_PQ = [yQ,yP];

 plot(x_AO,y_AO,x_BA,y_BA,x_BC,y_BC,x_PA,y_PA,x_QA,y_QA,x_PQ,y_PQ)
 set(gca(),"data_bounds",[xQ-10,yC-10;xO+50,yP+10]);
 mtlb_axis('equal');

end;

theta = (theta .*180)/%pi;
