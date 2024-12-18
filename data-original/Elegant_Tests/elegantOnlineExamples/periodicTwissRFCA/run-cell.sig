SDDS1
!# big-endian
&description text="sigma matrix--input: run-cell.ele  lattice: linac.lte", contents="sigma matrix", &end
&parameter name=Step, description="Simulation step", type=long, &end
&column name=s, units=m, description=Distance, type=double,  &end
&column name=ElementName, description="Element name", format_string=%10s, type=string,  &end
&column name=ElementOccurence, description="Occurence of element", format_string=%6ld, type=long,  &end
&column name=ElementType, description="Element-type name", format_string=%10s, type=string,  &end
&column name=s1, symbol="$gs$r$b1$n", units=m, description="sqrt(<x*x>)", type=double,  &end
&column name=s12, symbol="$gs$r$b12$n", units=m, description="<x*xp'>", type=double,  &end
&column name=s13, symbol="$gs$r$b13$n", units="m$a2$n", description="<x*y>", type=double,  &end
&column name=s14, symbol="$gs$r$b14$n", units=m, description="<x*y'>", type=double,  &end
&column name=s15, symbol="$gs$r$b15$n", units="m$a2$n", description="<x*s>", type=double,  &end
&column name=s16, symbol="$gs$r$b16$n", units=m, description="<x*delta>", type=double,  &end
&column name=s17, symbol="$gs$r$b17$n", units="m*s", description="<x*t>", type=double,  &end
&column name=s2, symbol="$gs$r$b2$n", description="sqrt(<x'*x'>)", type=double,  &end
&column name=s23, symbol="$gs$r$b23$n", units=m, description="<x'*y>", type=double,  &end
&column name=s24, symbol="$gs$r$b24$n", description="<x'*y'>", type=double,  &end
&column name=s25, symbol="$gs$r$b25$n", units=m, description="<x'*s>", type=double,  &end
&column name=s26, symbol="$gs$r$b26$n", description="<x'*delta>", type=double,  &end
&column name=s27, symbol="$gs$r$b27$n", units=s, description="<x'*t>", type=double,  &end
&column name=s3, symbol="$gs$r$b3$n", units=m, description="sqrt(<y*y>)", type=double,  &end
&column name=s34, symbol="$gs$r$b34$n", units=m, description="<y*y'>", type=double,  &end
&column name=s35, symbol="$gs$r$b35$n", units="m$a2$n", description="<y*s>", type=double,  &end
&column name=s36, symbol="$gs$r$b36$n", units=m, description="<y*delta>", type=double,  &end
&column name=s37, symbol="$gs$r$b37$n", units="m*s", description="<y*t>", type=double,  &end
&column name=s4, symbol="$gs$r$b4$n", description="sqrt(<y'*y')>", type=double,  &end
&column name=s45, symbol="$gs$r$b45$n", units=m, description="<y'*s>", type=double,  &end
&column name=s46, symbol="$gs$r$b46$n", description="<y'*delta>", type=double,  &end
&column name=s47, symbol="$gs$r$b47$n", units=s, description="<y'*t>", type=double,  &end
&column name=s5, symbol="$gs$r$b5$n", units=m, description="sqrt(<s*s>)", type=double,  &end
&column name=s56, symbol="$gs$r$b56$n", units=m, description="<s*delta>", type=double,  &end
&column name=s57, symbol="$gs$r$b57$n", units="m*s", description="<s*t>", type=double,  &end
&column name=s6, symbol="$gs$r$b6$n", description="sqrt(<delta*delta>)", type=double,  &end
&column name=s67, symbol="$gs$r$b67$n", units=s, description="<delta*t>", type=double,  &end
&column name=s7, symbol="$gs$r$b7$n", description="sqrt(<t*t>)", type=double,  &end
&column name=ma1, symbol="max$sb$ex$sb$e", units=m, description="maximum absolute value of x", type=double,  &end
&column name=ma2, symbol="max$sb$ex'$sb$e", description="maximum absolute value of x'", type=double,  &end
&column name=ma3, symbol="max$sb$ey$sb$e", units=m, description="maximum absolute value of y", type=double,  &end
&column name=ma4, symbol="max$sb$ey'$sb$e", description="maximum absolute value of y'", type=double,  &end
&column name=ma5, symbol="max$sb$e$gD$rs$sb$e", units=m, description="maximum absolute deviation of s", type=double,  &end
&column name=ma6, symbol="max$sb$e$gd$r$sb$e", description="maximum absolute value of delta", type=double,  &end
&column name=ma7, symbol="max$sb$e$gD$rt$sb$e", units=s, description="maximum absolute deviation of t", type=double,  &end
&column name=minimum1, symbol="x$bmin$n", units=m, type=double,  &end
&column name=minimum2, symbol="x'$bmin$n", units=m, type=double,  &end
&column name=minimum3, symbol="y$bmin$n", units=m, type=double,  &end
&column name=minimum4, symbol="y'$bmin$n", units=m, type=double,  &end
&column name=minimum5, symbol="$gD$rs$bmin$n", units=m, type=double,  &end
&column name=minimum6, symbol="$gd$r$bmin$n", units=m, type=double,  &end
&column name=minimum7, symbol="t$bmin$n", units=s, type=double,  &end
&column name=maximum1, symbol="x$bmax$n", units=m, type=double,  &end
&column name=maximum2, symbol="x'$bmax$n", units=m, type=double,  &end
&column name=maximum3, symbol="y$bmax$n", units=m, type=double,  &end
&column name=maximum4, symbol="y'$bmax$n", units=m, type=double,  &end
&column name=maximum5, symbol="$gD$rs$bmax$n", units=m, type=double,  &end
&column name=maximum6, symbol="$gd$r$bmax$n", units=m, type=double,  &end
&column name=maximum7, symbol="t$bmax$n", units=s, type=double,  &end
&column name=Sx, symbol="$gs$r$bx$n", units=m, description=sqrt(<(x-<x>)^2>), type=double,  &end
&column name=Sxp, symbol="$gs$r$bx'$n", description=sqrt(<(x'-<x'>)^2>), type=double,  &end
&column name=Sy, symbol="$gs$r$by$n", units=m, description=sqrt(<(y-<y>)^2>), type=double,  &end
&column name=Syp, symbol="$gs$r$by'$n", description=sqrt(<(y'-<y'>)^2>), type=double,  &end
&column name=Ss, symbol="$gs$r$bs$n", units=m, description=sqrt(<(s-<s>)^2>), type=double,  &end
&column name=Sdelta, symbol="$gs$bd$n$r", description=sqrt(<(delta-<delta>)^2>), type=double,  &end
&column name=St, symbol="$gs$r$bt$n", units=s, description=sqrt(<(t-<t>)^2>), type=double,  &end
&column name=ex, symbol="$ge$r$bx$n", units=m, description="geometric horizontal emittance", type=double,  &end
&column name=enx, symbol="$ge$r$bx,n$n", units=m, description="normalized horizontal emittance", type=double,  &end
&column name=ecx, symbol="$ge$r$bx,c$n", units=m, description="geometric horizontal emittance less dispersive contributions", type=double,  &end
&column name=ecnx, symbol="$ge$r$bx,cn$n", units=m, description="normalized horizontal emittance less dispersive contributions", type=double,  &end
&column name=ey, symbol="$ge$r$by$n", units=m, description="geometric vertical emittance", type=double,  &end
&column name=eny, symbol="$ge$r$by,n$n", units=m, description="normalized vertical emittance", type=double,  &end
&column name=ecy, symbol="$ge$r$by,c$n", units=m, description="geometric vertical emittance less dispersive contributions", type=double,  &end
&column name=ecny, symbol="$ge$r$by,cn$n", units=m, description="normalized vertical emittance less dispersive contributions", type=double,  &end
&column name=betaxBeam, symbol="$gb$r$bx,beam$n", units=m, description="betax for the beam, excluding dispersive contributions", type=double,  &end
&column name=alphaxBeam, symbol="$ga$r$bx,beam$n", description="alphax for the beam, excluding dispersive contributions", type=double,  &end
&column name=betayBeam, symbol="$gb$r$by,beam$n", units=m, description="betay for the beam, excluding dispersive contributions", type=double,  &end
&column name=alphayBeam, symbol="$ga$r$by,beam$n", description="alphay for the beam, excluding dispersive contributions", type=double,  &end
&data mode=binary, &end
   
              _BEG_      MARK?):o��-k=��G�vn=�I��~Pk<񗼫���                        >��Q��u�=f�H �x�����i�                        ?!�
��F=X/�k��                        ?�Ť�"                                                                        ?C;�;���?=����6?;sI��7G?�`���^                        �C;�;��ݿ=����6�;sI��7G��`���^                        ?C;�;���?=����6?;sI��7G?�`���^                        ?):o��-k>��Q��u�?!�
��F?�Ť�"                        >5�~|1B�>������a>5�~|1B�>������a>5�~|1C>�������>5�~|1C>�������@���V8���{�So�m@Z�∧���R�� ?�������   Q1H      QUAD?)��q�.�ϸ�=�F�d�p=���˳˚                        ? ��r�s��e�L��O��QV�Jg�                        ?"P83x�>!k�0A�h                        ?�v�                                                                        ?CK��B?!wth?;��w�?#�pN�Da                        �CK��B�!wth�;��w��#�pN�Da                        ?CK��B?!wth?;��w�?#�pN�Da                        ?)��q? ��r�s?"P83x�?�v�                        >5�~|1B�>������b>5�~|1B�>������b>5�~|1C>�������>5�~|1C>�������@���LC?��n��m@��E�i���f|���C?ə�����   L1      DRIF?(���t�-*�k�f�=�8j=��=���ߎ                        ? ��r�s��:�Z�(彲QV�Jg�                        ?">g���f>"�q�Ҙ                        ?�v�                                                                        ?CK���zQ?!wth?<�^�bU?#�pN�Da                        �CK���zQ�!wth�<�^�bU�#�pN�Da                        ?CK���zQ?!wth?<�^�bU?#�pN�Da                        ?(���t? ��r�s?">g���f?�v�                        >5�~|1B�>������a>5�~|1B�>������a>5�~|1C>�������>5�~|1C>�������@1�E�Z�?�C�� Ώ@T�z�g���e�B�Y@	������   LINA10      RFCA? ���AÈ��lP��=�����S���CG7��dP�ܜM������h�_uMUi>��Y�e1���b
���÷S���JK۠�&��6	V���E��n��O�;?&���J�U>2��6+�        �g��9��7�Y�����? ��!R�9>%����ڸP�ܜM��vH@�q��>)	C� �=,�sgT:��=:�W="ucQ��z���c�<fj���?@���u�9?���?G9�
��?��/J�>XĠ�   =G���7�<�-u�   �@���u�9�����G9�
�����/Jܾ*^��   �G���7ּg��@   ?@���u�9?���?G9�
��?��/J�>XĠ�   <�TT�(��<�-u�   ? ���AÈ>��Y�e1?&���J�U? ��!R�>)	C� ="ucQ�<fj���>-���n��>������k>-���n��>������k>-���n��>�������>-���n��>�������@��KUq�?�Y���@!���ऒ��1:Z"@
fffffg   L1      DRIF? �m�����N<�҇�=��QJ���r�4,69m)�r\=�8C�*0U2a���0�7�>��Y�e1�́5*�i9��÷S���JK۠�&��6	V���E7Q
8�C?'L�v9m>3%��׈�9e�^N�8D����h�H@�q��? ��!R�9>%����ڸP�ܜM���6��C->)	C� �=,�sgT:��=26�="ucQ��z��޶<fj��t �?@��VnG?���?G�ҝ�[j?��/J�>XĠ�   =G���7�<�-u�   �@��VnG�����G�ҝ�[j���/Jܾ*^��   �G���7ּg��@   ?@��VnG?���?G�ҝ�[j?��/J�>XĠ�   <�TT�(��<�-u�   ? �m���>��Y�e1?'L�v9m? ��!R�>)	C� ="ucQ�<fj��t �>-���n��>������k>-���n��>������k>-���n��>�������>-���n��>�������@��;�]?��r�\�@"M��Y`����(�lV@333334   Q2H      QUAD? �H�"I>;���L=�Iи�x���OG������h�K�nC�y�7�
8�C>���7��z��4��S���*
{19S�x�7�P�ܜM�7d����h�?'�$z{>ڬ"\�9bY����ҸVH@�q��7��*0U2a>���C&��9DP�ܜM�        �s�*0U2a>)	C���=,�sgT:��=�="ucQ��z�龎�<fj��Kѷ?@�q5O!�?�uԊ�e?G�h���?xHe���>Xġ    =G���7�<�-u�   �@�q5O!���uԊ�e�G�h��ؿxHe��ؾ*^��   �G���7ּg��@   ?@�q5O!�?�uԊ�e?G�h���?xHe���>Xġ    <�TT�(��<�-u�   ? �H�"I>���7��z?'�$z{>���C&��>)	C��="ucQ�<fj��Kѷ>-���n��>������j>-���n��>������j>-���n��>�������>-���n��>�������@�}�<l��%��H�@"����L�ب�j��}@        Q2H      QUAD? ��-٘�>+!�s�'j=����!Uu��~�A�OuMUi84����h�        ?�׆-���1ʴ.���\^�9����h�6��C-�OuMUi?'~Bn'*��J�u#�9i� ���8$����h�Ov_خ>�갚҂��;�W}�W8��n/�i�E��
�>)	C���=,�sgT:��<��X="ucQ��z��Q�<fj�� {�?A �(�s�?M����?G��=�d?=�� L>Xġ    =G���7�<�-u�   �A �(�s��M�����G��=�d�=�� L�*^��   �G���7ּg��    ?A �(�s�?M����?G��=�d?=�� L>Xġ    <�TT�(��<�-u�   ? ��-٘�?�׆-�?'~Bn'*�>�갚҂�>)	C��="ucQ�<fj�� {�>-���n��>������i>-���n��>������i>-���n��>�������>-���n��>�������@S��Ka��Fb-�8�@"��{�?�&k�^@������   L1      DRIF?!@ў�'>,B����`��Mս��Rn���n�J�!�D��Ѣ7��J�!?�׆-��̀��5U����\^�9����h�6��C-7�6��C-?'[�� ���8M{�z`�V.	�8J6��C-7��
|[>�갚҂��;�W}�W8��n/�wh����b>)	C���=,�sgT:��<�zA="ucQ��z��,�<fj���	?Aa��z��?M����?G��Q_��?=�� L>Xġ    =G���7�<�-u�   �Aa��z���M�����G��Q_���=�� L�*^��   �G���7ּg��@   ?Aa��z��?M����?G��Q_��?=�� L>Xġ    <�TT�(��<�-u�   ?!@ў�'?�׆-�?'[�� �>�갚҂�>)	C��="ucQ�<fj���	>-���n��>������i>-���n��>������i>-���n��>�������>-���n��>�������@�C����}�K��@"e㸳|G?�����@fffffg   LINA10      RFCA?(�7b��>6V켣��8a�|y����$�:9d����h�g��9��������h�? s��@r��׭��0������K��9$����h�8����h�        ?!����q��(�!E�W��9���W��9����6��C->�@�2�h9Q�!laR*�% ����8��C�f�>1g@BQ��VZ�o+�[:������:=TS&��!��S��g<o*-�rH!?H�=��
?L@[wh?B ���?K?mD�2>a&��   =a2V�<��@   �H�=��
�L@[wh�B ��刿K?mD�2�6*��   �a2V׼s��   ?H�=��
?L@[wh?B ���?K?mD�2>a&��   =[���O<��@   ?(�7b��? s��@r?!����q>�@�2�h>1g@BQ�=TS&��!<o*-�rH!>&e#v.Mt>������>&e#v.Mt>������>&e#v.M�>�������>&e#v.M�>�������@+�rvD�A� �ii5@��iG�?�gh����@������   Q1H      QUAD?):o��\�>����D���^�nrK3��oS�?�9T����h�RY�����        >�n��$���|�"����,HWP09����h�
���?�зT����h�?!�^�>�4ak        8S�*0U2a��6��C->�άl�D�Ҳ��M�4����h�����h�>1g@BQ��VZ�o+�[:������=TS&��!��S���<o*-�e�?H�\ʹ5�??Q�61?B z���?n��3�>a&��   =a2V�<��@   �H�\ʹ5��?Q�61�B z����n��3��6*��   �a2V׼s��   ?H�\ʹ5�??Q�61?B z���?n��3�>a&��   =[���O<��@   ?):o��\�>�n��$�?!�^�>�άl>1g@BQ�=TS&��!<o*-�e�>&e#v.Mu>������>&e#v.Mu>������>&e#v.M�>�������>&e#v.M�>�������@,k}�g��������J�@�[Wd�����E