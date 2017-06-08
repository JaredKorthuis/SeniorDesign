surface
dots( float
Diam = 0.10, // dot diameter
Ks = 0.5,
Kd = 0.5,
Ka = .1,
roughness = 0.1;
color specularColor = color( 1, 1, 1 )
)
{
float up = 2. * u;
float vp = v;
float numinu = floor( up / (2*A) ;
float numinv = floor( vp / (2*B) ;
float u = numinu *2*A + A;
float v = numinv *2*B+B;
color dotColor = Cs;
if( mod( numinu+numinv, 2 ) == 0 )
{
float uc = numinu*Diam + Diam/2.;
float vc = numinv*Diam + Diam/2.;
up = up - uc;
vp = vp - vc;
point upvp = point( up, vp, 0. );
point cntr = point( 0., 0., 0. );
if( distance( upvp, cntr ) < Diam/2. )
{
dotColor = color( 1., .5, 0. ); // beaver orange?
}
}
varying vector Nf = faceforward( normalize( N ), I );
vector V = normalize( -I );
Oi = 1.;
Ci = Oi * ( dotColor * ( Ka * ambient() + Kd * diffuse(Nf) ) +
specularColor * Ks * specular( Nf, V, roughness ) );
}