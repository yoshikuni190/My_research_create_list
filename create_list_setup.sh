wget https://db.anemone.bio/fishsciname2japname_anemone.pl
cpan install LWP::UserAgent
pip install pandas reportlab
apt-get -y install fonts-ipafont-gothic
pip install pandas matplotlib reportlab
xz -d /content/community_qc_fishes1.tsv.xz
xz -d /content/community_qc_fishes2.tsv.xz
xz -d /content/community_qc_fishes3.tsv.xz
xz -d /content/community_qc_fishes1_NC.tsv.xz
perl fishsciname2japname_anemone.pl < community_qc_fishes1.tsv > community_qc_fishes_japanese1.tsv
perl fishsciname2japname_anemone.pl < community_qc_fishes2.tsv > community_qc_fishes_japanese2.tsv
perl fishsciname2japname_anemone.pl < community_qc_fishes3.tsv > community_qc_fishes_japanese3.tsv
perl fishsciname2japname_anemone.pl < community_qc_fishes4.tsv > community_qc_fishes_japanese4.tsv
perl fishsciname2japname_anemone.pl < community_qc_fishes1_NC.tsv > community_qc_fishes_japanese1_NC.tsv