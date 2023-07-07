from ftplib import FTP as ftp


with ftp("ftp.ensemblgenomes.org") as conn:
    conn.login()
    conn.cwd("pub/bacteria/release-56/fasta")
    conn.cwd("bacteria_0_collection")
    conn.retrlines('LIST')
    for i in range(1, 129):
        conn.cwd(f"../bacteria_{i}_collection")
        conn.retrlines('LIST')
    conn.quit()
